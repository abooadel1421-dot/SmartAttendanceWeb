# app/student/routes.py

from app.student import bp as student_bp
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.user import User, UserRole
from app.models.student import Student
from app.models.attendance_log import AttendanceLog, AttendanceStatus, FinalAttendanceStatus
from app.models.excuse import Excuse, ExcuseStatus
from app.models.card import Card
from app.forms.report import ExcuseForm
from app.models.notification import Notification
from app import db
from functools import wraps
from datetime import datetime, timedelta, date, time
import pytz

# 🟢 تعريف المنطقة الزمنية للمملكة العربية السعودية
SAUDIA_TZ = pytz.timezone('Asia/Riyadh')

# 🟢 دالة مساعدة لإنشاء التوقيت المحلي من التاريخ والوقت
def combine_date_time_to_saudia_tz(d_obj, t_obj):
    combined_dt = datetime.combine(d_obj, t_obj)
    return SAUDIA_TZ.localize(combined_dt).astimezone(pytz.utc)

# 🟢 دالة مساعدة لتحويل التوقيتات
def convert_timestamp_to_saudia_tz(dt_obj):
    """Converts a datetime object to Saudi Arabia timezone."""
    if dt_obj:
        if dt_obj.tzinfo is None:
            dt_obj = pytz.utc.localize(dt_obj)
        return dt_obj.astimezone(SAUDIA_TZ)
    return dt_obj

# Decorator لضمان أن المستخدم هو طالب ومسجل الدخول
def student_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.STUDENT:
            flash('غير مصرح لك بالوصول إلى هذه الصفحة.', 'danger')
            if current_user.is_authenticated:
                if current_user.role == UserRole.ADMIN:
                    return redirect(url_for('admin.index'))
                elif current_user.role == UserRole.TEACHER:
                    return redirect(url_for('teacher.dashboard'))
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    """لوحة تحكم الطالب الرئيسية"""
    student = Student.query.filter_by(user_id=current_user.id).first_or_404()
    
    # 🟢 جلب معلومات البطاقة
    card = Card.query.filter_by(student_id=student.id).first()

    # 🟢 حساب الإحصائيات المطلوبة في القالب
    # 1. عدد مرات الغياب
    absent_count = AttendanceLog.query.filter_by(
        student_id=student.id, 
        final_status=FinalAttendanceStatus.ABSENT
    ).count()
    
    # 2. عدد مرات التأخير
    late_arrivals_count = AttendanceLog.query.filter_by(
        student_id=student.id, 
        final_status=FinalAttendanceStatus.LATE
    ).count()

    # 3. عدد أيام الحضور الفريدة
    distinct_present_days = db.session.query(
        db.func.count(db.distinct(db.func.date(AttendanceLog.timestamp)))
    ).filter(
        AttendanceLog.student_id == student.id,
        AttendanceLog.final_status == FinalAttendanceStatus.PRESENT
    ).scalar() or 0

    # 4. نسبة الحضور
    total_relevant_entries = AttendanceLog.query.filter(
        AttendanceLog.student_id == student.id,
        AttendanceLog.final_status.in_([
            FinalAttendanceStatus.PRESENT, 
            FinalAttendanceStatus.ABSENT, 
            FinalAttendanceStatus.LATE, 
            FinalAttendanceStatus.EXCUSED
        ])
    ).count()

    # عدد الحالات التي تعتبر "حضور"
    present_or_excused_count = AttendanceLog.query.filter(
        AttendanceLog.student_id == student.id,
        AttendanceLog.final_status.in_([
            FinalAttendanceStatus.PRESENT, 
            FinalAttendanceStatus.EXCUSED
        ])
    ).count()
    
    attendance_percentage = 0
    if total_relevant_entries > 0:
        attendance_percentage = round((present_or_excused_count / total_relevant_entries) * 100, 2)
    
    # 🟢 آخر سجلات الحضور
    attendance_logs_raw = AttendanceLog.query.filter_by(student_id=student.id)\
                                     .order_by(AttendanceLog.timestamp.desc())\
                                     .limit(5).all()
    
    attendance_logs_processed = []
    for log in attendance_logs_raw:
        log.timestamp = convert_timestamp_to_saudia_tz(log.timestamp)
        if not log.device:
            log.device = None
        attendance_logs_processed.append(log)

    # 🟢 جلب جميع الإشعارات للطالب
    notifications_raw = Notification.query.filter_by(receiver_id=current_user.id)\
                                             .order_by(Notification.timestamp.desc())\
                                             .all()
    
    notifications_processed = []
    for notif in notifications_raw:
        notif.timestamp = convert_timestamp_to_saudia_tz(notif.timestamp)
        if not notif.sender:
            notif.sender = None
        notifications_processed.append(notif)
    
    # 🟢 حساب عدد الإشعارات غير المقروءة
    unread_notifications_count = Notification.query.filter_by(
        receiver_id=current_user.id, 
        status='unread'
    ).count()

    return render_template('student/dashboard.html',
                           title="لوحة تحكم الطالب",
                           student=student,
                           card=card,
                           absent_count=absent_count,
                           late_arrivals_count=late_arrivals_count,
                           distinct_present_days=distinct_present_days,
                           attendance_percentage=attendance_percentage,
                           attendance_logs=attendance_logs_processed,
                           notifications=notifications_processed,
                           unread_notifications_count=unread_notifications_count,
                           FinalAttendanceStatus=FinalAttendanceStatus)

@student_bp.route('/my_attendance')
@login_required
@student_required
def my_attendance():
    """عرض سجلات حضور وغياب الطالب مع إمكانية تقديم عذر"""
    student = Student.query.filter_by(user_id=current_user.id).first_or_404()

    attendance_records_raw = AttendanceLog.query.filter(
        AttendanceLog.student_id == student.id,
        AttendanceLog.final_status.isnot(None)
    ).options(db.joinedload(AttendanceLog.device)).order_by(AttendanceLog.timestamp.desc()).all()

    attendance_records_processed = []
    for record in attendance_records_raw:
        # تحويل timestamp للسجل إلى توقيت السعودية
        record.timestamp = convert_timestamp_to_saudia_tz(record.timestamp)
        
        # البحث عن عذر سابق لهذا التاريخ
        existing_excuse = Excuse.query.filter_by(
            student_id=student.id,
            date_of_absence=record.timestamp.date()
        ).first()

        # حساب وقت الدخول الفعلي
        actual_entry_time = None
        
        # تحديد بداية ونهاية اليوم بتوقيت UTC
        day_start_utc = SAUDIA_TZ.localize(datetime.combine(record.timestamp.date(), time.min)).astimezone(pytz.utc)
        day_end_utc = SAUDIA_TZ.localize(datetime.combine(record.timestamp.date(), time.max)).astimezone(pytz.utc)

        # البحث عن أول سجل دخول
        first_entry_for_day = AttendanceLog.query.filter(
            AttendanceLog.student_id == student.id,
            AttendanceLog.timestamp >= day_start_utc,
            AttendanceLog.timestamp <= day_end_utc,
            AttendanceLog.status == AttendanceStatus.ENTER
        ).order_by(AttendanceLog.timestamp.asc()).first()

        if first_entry_for_day:
            actual_entry_time = convert_timestamp_to_saudia_tz(first_entry_for_day.timestamp).time()

        attendance_records_processed.append({
            'log': record,
            'excuse': existing_excuse,
            'actual_entry_time': actual_entry_time
        })

    # فلترة السجلات لتقديم العذر
    dates_with_excuse = {
        e.date_of_absence for e in Excuse.query.filter_by(
            student_id=student.id, 
            status=ExcuseStatus.APPROVED
        ).all()
    }
    
    # قائمة بالأيام التي يمكن للطالب تقديم عذر عنها
    absent_dates_for_excuse = []
    processed_dates = set()

    for record_entry in attendance_records_processed:
        log = record_entry['log']
        excuse = record_entry['excuse']
        record_date = log.timestamp.date()
        
        if log.final_status == FinalAttendanceStatus.ABSENT and \
           (not excuse or excuse.status != ExcuseStatus.APPROVED) and \
           record_date not in processed_dates:
            absent_dates_for_excuse.append(record_date)
            processed_dates.add(record_date)
    
    absent_dates_for_excuse.sort(reverse=True)

    return render_template('student/my_attendance.html',
                           title="سجل الحضور والغياب",
                           student=student,
                           attendance_records=attendance_records_processed,
                           absent_dates_for_excuse=absent_dates_for_excuse,
                           FinalAttendanceStatus=FinalAttendanceStatus,
                           ExcuseStatus=ExcuseStatus)

@student_bp.route('/submit_excuse', methods=['GET', 'POST'])
@login_required
@student_required
def submit_excuse():
    """تقديم عذر للغياب أو التأخر"""
    student = Student.query.filter_by(user_id=current_user.id).first_or_404()
    form = ExcuseForm()

    # يمكن تعبئة تاريخ الغياب مسبقًا إذا تم إرساله كمعامل
    prefill_date = request.args.get('date')
    if prefill_date:
        try:
            form.date_of_absence.data = datetime.strptime(prefill_date, '%Y-%m-%d').date()
        except ValueError:
            flash('تاريخ غير صالح في الرابط.', 'danger')
            return redirect(url_for('student.my_attendance'))

    if form.validate_on_submit():
        # التحقق: هل يوجد عذر بالفعل في هذا التاريخ؟
        existing_excuse = Excuse.query.filter_by(
            student_id=student.id,
            date_of_absence=form.date_of_absence.data
        ).first()

        if existing_excuse:
            flash('لقد قدمت عذراً بالفعل لهذا التاريخ.', 'warning')
            return render_template('student/submit_excuse.html', title='تقديم عذر', form=form)

        new_excuse = Excuse(
            student_id=student.id,
            date_of_absence=form.date_of_absence.data,
            reason=form.reason.data,
            status=ExcuseStatus.PENDING,
            submitted_at=datetime.now(pytz.utc)
        )
        db.session.add(new_excuse)
        db.session.commit()
        
        # 🟢 إرسال إشعار للمدرس بوجود عذر جديد
        teachers = User.query.filter_by(role=UserRole.TEACHER).all()
        for teacher_user in teachers:
            if teacher_user:
                notification_message = f"تم تقديم عذر جديد من الطالب {student.full_name} لتاريخ {form.date_of_absence.data.strftime('%Y-%m-%d')}."
                new_notification_to_teacher = Notification(
                    sender_id=current_user.id,
                    receiver_id=teacher_user.id,
                    message=notification_message,
                    status='unread',
                    type='excuse_status'
                )
                db.session.add(new_notification_to_teacher)
        
        db.session.commit()
        
        flash('تم إرسال العذر بنجاح، وسنقوم بمراجعته قريباً.', 'success')
        return redirect(url_for('student.my_attendance'))

    return render_template('student/submit_excuse.html', title='تقديم عذر', form=form)

@student_bp.route('/my_notifications')
@login_required
@student_required
def view_my_notifications():
    """عرض جميع إشعارات الطالب"""
    # تحميل علاقة sender لتجنب N+1 query problem
    notifications_raw = Notification.query.filter_by(receiver_id=current_user.id)\
                                           .options(db.joinedload(Notification.sender))\
                                           .order_by(Notification.timestamp.desc())\
                                           .all()
    
    notifications_processed = []
    for notif in notifications_raw:
        notif.timestamp = convert_timestamp_to_saudia_tz(notif.timestamp)
        notifications_processed.append(notif)
    
    # تحديث حالة الإشعارات إلى "مقروءة" عند عرضها
    unread_notifications = Notification.query.filter_by(
        receiver_id=current_user.id, 
        status='unread'
    ).all()
    
    for notif in unread_notifications:
        notif.status = 'read'
    
    db.session.commit()

    return render_template('student/my_notifications.html',
                           title='إشعاراتي',
                           notifications=notifications_processed)