# app/teacher/routes.py

from app.teacher import teacher_bp
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.user import User, UserRole
from app.models.student import Student
# 🟢 عدّل هذا السطر ليحتوي على جميع الاستيرادات المطلوبة من attendance_log
from app.models.attendance_log import AttendanceLog, AttendanceStatus, FinalAttendanceStatus 
from app.models.device import Device
from app.models.notification import Notification
from app.forms.notification import SendNotificationForm 

from app import db
from functools import wraps
from datetime import datetime, timedelta, date, time # 🟢 أضف 'time' هنا
import pytz

from app.models.excuse import Excuse, ExcuseStatus 
from app.forms.report import GenerateAttendanceReportForm, UpdateAttendanceStatusForm 

import pytz
from datetime import datetime, timedelta
# تأكد من استيراد النماذج والمكثفات الضرورية
from flask import render_template, current_app
from flask_login import login_required, current_user
# تأكد من استيراد blueprints والنموذج AttendanceLog و AttendanceStatus
from app.teacher import teacher_bp
from app.models import Student, AttendanceLog, AttendanceStatus # تأكد من أن AttendanceStatus مستورد
from app.utils.helpers import convert_timestamp_to_saudia_tz # تأكد من مسار الدالة

# 🟢 تعريف المنطقة الزمنية للمملكة العربية السعودية
SAUDIA_TZ = pytz.timezone('Asia/Riyadh')

# 🟢 إضافة دالة مساعدة لإنشاء التوقيت المحلي من التاريخ والوقت
def combine_date_time_to_saudia_tz(d_obj, t_obj):
    combined_dt = datetime.combine(d_obj, t_obj)
    return SAUDIA_TZ.localize(combined_dt).astimezone(pytz.utc) # تحويل إلى UTC للحفظ في DB

# Decorator لضمان أن المستخدم هو معلم ومسجل الدخول
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != UserRole.TEACHER:
            flash('غير مصرح لك بالوصول إلى هذه الصفحة.', 'danger')
            if current_user.is_authenticated:
                if current_user.role == UserRole.ADMIN:
                    return redirect(url_for('admin.index'))
                elif current_user.role == UserRole.STUDENT:
                    return redirect(url_for('student.dashboard'))
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# 🟢 دالة مساعدة لتحويل التوقيتات (لتجنب تكرار الكود)
def convert_timestamp_to_saudia_tz(dt_obj):
    """Converts a datetime object to Saudi Arabia timezone."""
    if dt_obj:
        if dt_obj.tzinfo is None:
            # Assume it's UTC if no timezone info, then localize
            dt_obj = pytz.utc.localize(dt_obj)
        return dt_obj.astimezone(SAUDIA_TZ)
    return dt_obj


@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    """لوحة تحكم المعلم الرئيسية"""
    
    # 🟢 تحديد بداية ونهاية اليوم بتوقيت الرياض ثم تحويلها إلى UTC للمقارنة مع DB
    now_saudia = datetime.now(SAUDIA_TZ)
    start_of_day_saudia = now_saudia.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day_saudia = start_of_day_saudia + timedelta(days=1) - timedelta(microseconds=1)

    start_of_day_utc = start_of_day_saudia.astimezone(pytz.utc)
    end_of_day_utc = end_of_day_saudia.astimezone(pytz.utc)
    
    # إحصائيات اليوم
    total_students = Student.query.count()
    
    # 🟢 استخدام start_of_day_utc و end_of_day_utc للفلترة
    today_logs_raw = AttendanceLog.query.filter(
        AttendanceLog.timestamp >= start_of_day_utc,
        AttendanceLog.timestamp <= end_of_day_utc
    ).all()
    
    # لحساب الطلاب الحاضرين الفريدين
    present_students_ids = {log.student_id for log in today_logs_raw if log.status == AttendanceStatus.ENTER}
    present_today_unique = len(present_students_ids)
    
    # حساب الغائبين
    absent_today = total_students - present_today_unique
    
    # آخر السجلات
    recent_logs_raw = AttendanceLog.query.order_by(
        AttendanceLog.timestamp.desc()
    ).limit(10).all()
    
    # 🟢 معالجة التوقيتات في recent_logs
    recent_logs_processed = []
    for log in recent_logs_raw:
        # هنا نستدعي الدالة المساعدة convert_timestamp_to_saudia_tz
        log.timestamp = convert_timestamp_to_saudia_tz(log.timestamp)
        
        # --- أضف هذه الأسطر الجديدة للطباعة ---
        current_app.logger.debug(f"Log ID: {log.id}, Student ID: {log.student_id}, Timestamp: {log.timestamp}")
        current_app.logger.debug(f"Status: {log.status}, Status Value: {log.status.value if log.status else 'N/A'}")
        current_app.logger.debug(f"Location: {log.location if log.location else 'N/A (None or Empty)'}")
        # ------------------------------------
        
        recent_logs_processed.append(log)
    
    return render_template('teacher/dashboard.html',
                          title="لوحة تحكم المعلم",
                          total_students=total_students,
                          present_today=present_today_unique, # 🟢 استخدام العدد الفريد
                          absent_today=absent_today,
                          total_logs_today=len(today_logs_raw),
                          recent_logs=recent_logs_processed)


@teacher_bp.route('/students')
@login_required
@teacher_required
def view_students():
    """عرض قائمة الطلاب"""
    page = request.args.get('page', 1, type=int)
    students_pagination = Student.query.paginate(
        page=page, per_page=15, error_out=False
    )
    
    return render_template('teacher/students_list.html',
                          title="قائمة الطلاب",
                          students=students_pagination.items,
                          pagination=students_pagination)


@teacher_bp.route('/students/<int:student_id>')
@login_required
@teacher_required
def view_student_details(student_id):
    """عرض تفاصيل طالب واحد"""
    student = Student.query.get_or_404(student_id)
    
    # سجلات الحضور للطالب
    attendance_logs_raw = AttendanceLog.query.filter_by(
        student_id=student_id
    ).order_by(AttendanceLog.timestamp.desc()).limit(30).all()
    
    # 🟢 معالجة التوقيتات في attendance_logs
    attendance_logs_processed = []
    for log in attendance_logs_raw:
        log.timestamp = convert_timestamp_to_saudia_tz(log.timestamp)
        attendance_logs_processed.append(log)
    
    # إحصائيات الحضور
    total_logs = AttendanceLog.query.filter_by(student_id=student_id).count()
    enter_count = sum(1 for log in attendance_logs_raw if log.status == AttendanceStatus.ENTER)
    exit_count = sum(1 for log in attendance_logs_raw if log.status == AttendanceStatus.EXIT)
    
    return render_template('teacher/student_details.html',
                          title=f'تفاصيل الطالب: {student.full_name}',
                          student=student,
                          attendance_logs=attendance_logs_processed,
                          total_logs=total_logs,
                          enter_count=enter_count,
                          exit_count=exit_count)


@teacher_bp.route('/attendance')
@login_required
@teacher_required
def attendance_records():
    """عرض سجلات الحضور"""
    date_from_str = request.args.get('date_from')
    date_to_str = request.args.get('date_to')
    student_id = request.args.get('student_id')
    
    query = AttendanceLog.query.options(
        db.joinedload(AttendanceLog.student),
        db.joinedload(AttendanceLog.device)
    )
    
    if date_from_str:
        start_date_local = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        start_datetime_local_aware = SAUDIA_TZ.localize(datetime.combine(start_date_local, datetime.min.time()))
        start_datetime_utc = start_datetime_local_aware.astimezone(pytz.utc)
        query = query.filter(AttendanceLog.timestamp >= start_datetime_utc)
    
    if date_to_str:
        end_date_local = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        end_datetime_local_aware = SAUDIA_TZ.localize(datetime.combine(end_date_local, datetime.max.time()))
        end_datetime_utc = end_datetime_local_aware.astimezone(pytz.utc)
        query = query.filter(AttendanceLog.timestamp <= end_datetime_utc)
    
    if student_id:
        query = query.filter(AttendanceLog.student_id == student_id)
    
    logs_raw = query.order_by(AttendanceLog.timestamp.desc()).all()
    
    # 🟢 معالجة التوقيتات في logs
    logs_processed = []
    for log in logs_raw:
        log.timestamp = convert_timestamp_to_saudia_tz(log.timestamp)
        logs_processed.append(log)

    students = Student.query.all()
    
    return render_template('teacher/attendance_records.html',
                          title='سجلات الحضور',
                          logs=logs_processed,
                          students=students,
                          date_from=date_from_str,
                          date_to=date_to_str,
                          selected_student_id=student_id)


@teacher_bp.route('/reports')
@login_required
@teacher_required
def view_reports():
    """عرض التقارير"""
    
    # 🟢 تحديد بداية الشهر بتوقيت الرياض ثم تحويلها إلى UTC
    now_saudia = datetime.now(SAUDIA_TZ)
    month_start_saudia = now_saudia.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_start_utc = month_start_saudia.astimezone(pytz.utc)
    
    # إحصائيات الشهر
    month_logs_raw = AttendanceLog.query.filter(
        AttendanceLog.timestamp >= month_start_utc
    ).all()
    
    # الطلاب الأكثر غياباً (هذه الإحصائيات لن تحتاج لتحويل التوقيتات للعرض المباشر، فقط للفلترة)
    students = Student.query.all()
    attendance_stats = []
    
    for student in students:
        # 🟢 جلب سجلات الطالب خلال الشهر الحالي (بتوقيت UTC)
        student_logs_in_month = AttendanceLog.query.filter(
            AttendanceLog.student_id == student.id,
            AttendanceLog.timestamp >= month_start_utc
        ).all()
        
        total_logs_for_student_in_month = len(student_logs_in_month)
        enter_count_in_month = sum(1 for log in student_logs_in_month if log.status == AttendanceStatus.ENTER)
        
        attendance_stats.append({
            'student': student,
            'total': total_logs_for_student_in_month,
            'present': enter_count_in_month,
            'absent': total_logs_for_student_in_month - enter_count_in_month
        })
    
    # ترتيب حسب الغياب
    attendance_stats.sort(key=lambda x: x['absent'], reverse=True)
    
    return render_template('teacher/reports.html',
                          title='التقارير',
                          attendance_stats=attendance_stats,
                          month_logs_count=len(month_logs_raw))


@teacher_bp.route('/api/daily-stats')
@login_required
@teacher_required
def api_daily_stats():
    """API لإحصائيات اليوم"""
    # 🟢 تحديد بداية ونهاية اليوم بتوقيت الرياض ثم تحويلها إلى UTC للمقارنة مع DB
    now_saudia = datetime.now(SAUDIA_TZ)
    start_of_day_saudia = now_saudia.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day_saudia = start_of_day_saudia + timedelta(days=1) - timedelta(microseconds=1)

    start_of_day_utc = start_of_day_saudia.astimezone(pytz.utc)
    end_of_day_utc = end_of_day_saudia.astimezone(pytz.utc)
    
    total_students = Student.query.count()
    today_logs_raw = AttendanceLog.query.filter(
        AttendanceLog.timestamp >= start_of_day_utc,
        AttendanceLog.timestamp <= end_of_day_utc
    ).all()
    
    present_students_ids = {log.student_id for log in today_logs_raw if log.status == AttendanceStatus.ENTER}
    present_today_unique = len(present_students_ids)
    absent_today = total_students - present_today_unique
    
    return jsonify({
        'success': True,
        'total_students': total_students,
        'present_today': present_today_unique,
        'absent_today': absent_today,
        'total_logs_today': len(today_logs_raw)
    })


@teacher_bp.route('/notifications')
@login_required
@teacher_required
def view_notifications():
    """عرض التنبيهات والملاحظات"""
    # 🟢 تحديد بداية ونهاية اليوم بتوقيت الرياض ثم تحويلها إلى UTC للمقارنة مع DB
    now_saudia = datetime.now(SAUDIA_TZ)
    start_of_day_saudia = now_saudia.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day_saudia = start_of_day_saudia + timedelta(days=1) - timedelta(microseconds=1)

    start_of_day_utc = start_of_day_saudia.astimezone(pytz.utc)
    end_of_day_utc = end_of_day_saudia.astimezone(pytz.utc)
    
    all_students = Student.query.all()
    today_logs_raw = AttendanceLog.query.filter(
        AttendanceLog.timestamp >= start_of_day_utc,
        AttendanceLog.timestamp <= end_of_day_utc
    ).all()
    
    logged_students = {log.student_id for log in today_logs_raw if log.status == AttendanceStatus.ENTER}
    absent_students = [s for s in all_students if s.id not in logged_students]
    
    return render_template('teacher/notifications.html',
                          title='التنبيهات',
                          absent_students=absent_students)



@teacher_bp.route('/send_notification', methods=['GET', 'POST'])
@login_required
@teacher_required
def send_notification():
    form = SendNotificationForm()

    if form.validate_on_submit():
        student_id_selected = form.student_id.data
        if student_id_selected == 0: # إذا كان الخيار الافتراضي "اختر طالباً"
            flash('الرجاء اختيار طالب لإرسال الإشعار.', 'warning')
            return render_template('teacher/send_notification.html', title='إرسال إشعار', form=form)

        student = Student.query.get(student_id_selected)
        if not student:
            flash('الطالب المحدد غير موجود.', 'danger')
            return render_template('teacher/send_notification.html', title='إرسال إشعار', form=form)

        # 🟢 هذا هو التعديل الأساسي
        # الوصول إلى كائن User المرتبط بالطالب عبر العلاقة 'user_account'
        student_user = student.user_account
        
        if not student_user:
            flash('لا يوجد حساب مستخدم مرتبط بهذا الطالب. يرجى التأكد من ربط الطالب بحساب مستخدم.', 'danger')
            return render_template('teacher/send_notification.html', title='إرسال إشعار', form=form)

        new_notification = Notification(
            sender_id=current_user.id, # المعلم الحالي هو المرسل
            receiver_id=student_user.id, # حساب المستخدم للطالب هو المستلم
            message=form.message.data,
            status='unread',
            type='general'
        )
        db.session.add(new_notification)
        db.session.commit()
        flash('تم إرسال الإشعار بنجاح!', 'success')
        return redirect(url_for('teacher.send_notification')) # أو إعادة التوجيه إلى صفحة أخرى

    return render_template('teacher/send_notification.html', title='إرسال إشعار', form=form)


# 🟢 إضافة نقطة نهاية لعرض الإشعارات التي أرسلها المعلم
@teacher_bp.route('/teacher_notifications')
@login_required
@teacher_required
def teacher_notifications():
    sent_notifications_raw = Notification.query.filter_by(sender_id=current_user.id)\
                                           .order_by(Notification.timestamp.desc())\
                                           .all()
    
    # 🟢 معالجة التوقيتات في الإشعارات المرسلة
    sent_notifications_processed = []
    for notif in sent_notifications_raw:
        notif.timestamp = convert_timestamp_to_saudia_tz(notif.timestamp)
        sent_notifications_processed.append(notif)

    return render_template('teacher/teacher_notifications.html', 
                           title='إشعاراتي المرسلة', 
                           notifications=sent_notifications_processed)
    
    

# 🟢🟢🟢 أضف هذا الجزء الجديد هنا 🟢🟢🟢
# 🟢 تحديث دالة manage_excuses لتوفير البيانات للقالب
@teacher_bp.route('/manage_excuses')
@login_required
@teacher_required
def manage_excuses():
    """إدارة الأعذار المقدمة من الطلاب"""
    # جلب الأعذار قيد المراجعة
    pending_excuses_raw = Excuse.query.filter_by(status=ExcuseStatus.PENDING)\
                                  .options(db.joinedload(Excuse.student))\
                                  .order_by(Excuse.submitted_at.desc())\
                                  .all()

    # جلب الأعذار المعتمدة (آخر 5 مثلاً)
    approved_excuses_raw = Excuse.query.filter_by(status=ExcuseStatus.APPROVED)\
                                   .options(db.joinedload(Excuse.student), db.joinedload(Excuse.reviewer))\
                                   .order_by(Excuse.reviewed_at.desc())\
                                   .limit(5).all()

    # جلب الأعذار المرفوضة (آخر 5 مثلاً)
    rejected_excuses_raw = Excuse.query.filter_by(status=ExcuseStatus.REJECTED)\
                                   .options(db.joinedload(Excuse.student), db.joinedload(Excuse.reviewer))\
                                   .order_by(Excuse.reviewed_at.desc())\
                                   .limit(5).all()

    # تحويل التوقيتات للعرض
    pending_excuses = []
    for excuse in pending_excuses_raw:
        excuse.submitted_at = convert_timestamp_to_saudia_tz(excuse.submitted_at)
        pending_excuses.append(excuse)

    approved_excuses = []
    for excuse in approved_excuses_raw:
        excuse.submitted_at = convert_timestamp_to_saudia_tz(excuse.submitted_at)
        if excuse.reviewed_at:
            excuse.reviewed_at = convert_timestamp_to_saudia_tz(excuse.reviewed_at)
        approved_excuses.append(excuse)

    rejected_excuses = []
    for excuse in rejected_excuses_raw:
        excuse.submitted_at = convert_timestamp_to_saudia_tz(excuse.submitted_at)
        if excuse.reviewed_at:
            excuse.reviewed_at = convert_timestamp_to_saudia_tz(excuse.reviewed_at)
        rejected_excuses.append(excuse)

    return render_template('teacher/manage_excuses.html',
                           title="إدارة أعذار الطلاب",
                           pending_excuses=pending_excuses,
                           approved_excuses=approved_excuses,
                           rejected_excuses=rejected_excuses)

@teacher_bp.route('/review_excuse/<int:excuse_id>', methods=['POST'])
@login_required
@teacher_required
def review_excuse(excuse_id):
    excuse = Excuse.query.get_or_404(excuse_id)
    action = request.form.get('action')
    review_notes = request.form.get('review_notes')

    if action == 'approve':
        excuse.status = ExcuseStatus.APPROVED
        notification_type = 'approved'  # String بدل Enum  # ✅ Enum
        message_text = f"تم قبول عذرك لغياب بتاريخ {excuse.date_of_absence.strftime('%Y-%m-%d')}."
        flash(f'تم قبول عذر الطالب {excuse.student.full_name} بتاريخ {excuse.date_of_absence.strftime("%Y-%m-%d")}.', 'success')
    elif action == 'reject':
        excuse.status = ExcuseStatus.REJECTED
        notification_type = 'rejected'  # String
        message_text = f"تم رفض عذرك لغياب بتاريخ {excuse.date_of_absence.strftime('%Y-%m-%d')}."
        flash(f'تم رفض عذر الطالب {excuse.student.full_name} بتاريخ {excuse.date_of_absence.strftime("%Y-%m-%d")}.', 'danger')
    else:
        flash('إجراء غير صالح.', 'danger')
        return redirect(url_for('teacher.manage_excuses'))

    excuse.reviewer_id = current_user.id
    excuse.reviewed_at = datetime.utcnow()
    excuse.review_notes = review_notes

    # تحديث سجل الحضور إذا كان معتمداً
    if excuse.status == ExcuseStatus.APPROVED:
        absent_log = AttendanceLog.query.filter(
            AttendanceLog.student_id == excuse.student_id,
            db.func.date(AttendanceLog.timestamp) == excuse.date_of_absence,
            AttendanceLog.final_status == FinalAttendanceStatus.ABSENT
        ).first()

        if absent_log:
            absent_log.final_status = FinalAttendanceStatus.EXCUSED
            db.session.add(absent_log)

    # ✅ إنشاء إشعار صحيح
    student_user = User.query.get(excuse.student.user_id)
    if student_user:
        student_notification = Notification(
            receiver_id=student_user.id,
            sender_id=current_user.id,
            message=message_text,
            type=notification_type,  # String (excuse_approved أو excuse_rejected)
            status='unread',  # ✅ Enum value
        )
        db.session.add(student_notification)

    db.session.add(excuse)
    db.session.commit()

    return redirect(url_for('teacher.manage_excuses'))
# 🟢 دالة لتحديد جميع الإشعارات كمقروءة للمعلم الحالي
@teacher_bp.route('/mark_all_notifications_read')
@login_required
@teacher_required
def mark_all_notifications_read():
    # ✅ استخدم .value عند المقارنة في filter_by
    notifications_to_mark = Notification.query.filter_by(
        receiver_id=current_user.id,
        status='unread'
    ).all()
    
    for notif in notifications_to_mark:
        notif.status = 'read'
    
    db.session.commit()
    flash('تم تحديد جميع الإشعارات كمقروءة.', 'info')
    return redirect(url_for('teacher.dashboard'))

@teacher_bp.route('/update_excuse_status/<int:excuse_id>/<string:new_status>', methods=['POST'])
@login_required
@teacher_required
def update_excuse_status(excuse_id, new_status):
    excuse = Excuse.query.get_or_404(excuse_id)
    
    try:
        status_enum = ExcuseStatus[new_status.upper()] # تحويل القيمة النصية إلى عضو Enum
        excuse.status = status_enum
        excuse.reviewed_by_id = current_user.id
        excuse.reviewed_at = datetime.now(pytz.utc)
        db.session.commit()
        flash(f'تم تحديث حالة العذر بنجاح إلى {status_enum.value}.', 'success')
    except KeyError:
        flash('حالة غير صالحة.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'حدث خطأ أثناء تحديث حالة العذر: {e}', 'danger')
    
    return redirect(url_for('teacher.manage_excuses'))

# 🟢🟢🟢 انتهاء الجزء الجديد 🟢🟢🟢



@teacher_bp.route('/generate_report', methods=['GET', 'POST'])
@login_required
@teacher_required
def generate_report():
    form = GenerateAttendanceReportForm()
    report_data = None
    report_date = None
    start_time_obj = None
    end_time_obj = None

    if form.validate_on_submit():
        report_date = form.report_date.data
        start_time_obj = form.start_time.data
        end_time_obj = form.end_time.data

        # 🟢 1. حساب النقاط الزمنية الرئيسية لليوم المحدد بتوقيت الرياض 🟢
        
        # الوقت الفعلي لبدء الحضور (السماح بـ 30 دقيقة قبل الوقت المحدد من الفورم)
        dt_start_for_calc = datetime.combine(report_date, start_time_obj)
        effective_check_in_earliest_dt = dt_start_for_calc - timedelta(minutes=30)
        
        # الوقت النهائي للمتأخرين (حتى 10 دقائق بعد الوقت المحدد من الفورم)
        effective_check_in_latest_dt = dt_start_for_calc + timedelta(minutes=10)

        # نهاية الفترة الزمنية التي حددها المستخدم للتقرير (من الفورم)
        report_period_end_dt = datetime.combine(report_date, end_time_obj)

        # 🟢 2. تحديد نطاق البحث الفعلي عن سجلات الدخول في قاعدة البيانات (UTC) 🟢
        # هذا النطاق يحدد من أين نبدأ البحث عن سجلات الدخول وإلى أين ينتهي.
        # يجب أن يبدأ من أقدم وقت محتمل لتسجيل الدخول (بما في ذلك فترة السماح)
        # وينتهي عند أحدث وقت مسموح به ضمن فترة التقرير.
        
        # تحويل الأوقات الزمنية إلى كائنات datetime بـ SAUDIA_TZ ثم إلى UTC
        search_period_start_utc = SAUDIA_TZ.localize(effective_check_in_earliest_dt).astimezone(pytz.utc)
        search_period_end_utc = SAUDIA_TZ.localize(report_period_end_dt).astimezone(pytz.utc)
        
        # جلب جميع الطلاب
        all_students = Student.query.all()
        report_data = []

        for student in all_students:
            # 🟢 3. البحث عن أول سجل دخول للطالب ضمن نطاق البحث الدقيق (UTC) 🟢
            student_entry_log = AttendanceLog.query.filter(
                AttendanceLog.student_id == student.id,
                AttendanceLog.status == AttendanceStatus.ENTER,
                AttendanceLog.timestamp >= search_period_start_utc, # 👈 التعديل الرئيسي هنا
                AttendanceLog.timestamp <= search_period_end_utc    # 👈 والتعديل الرئيسي هنا
            ).order_by(AttendanceLog.timestamp.asc()).first() # نأخذ أول سجل دخول داخل هذا النطاق

            status = FinalAttendanceStatus.ABSENT # الحالة الافتراضية
            entry_time_saudia = None

            if student_entry_log:
                # إذا وجد سجل دخول، نحول وقته إلى توقيت الرياض للمقارنة مع أوقات التقرير
                entry_time_saudia = convert_timestamp_to_saudia_tz(student_entry_log.timestamp).time()

                # 🟢 4. تحديد الحالة بناءً على المنطق الجديد والقيم الزمنية المحسوبة (كائنات time فقط) 🟢
                # effective_check_in_earliest_dt.time() : بداية الـ 30 دقيقة قبل الموعد
                # start_time_obj : وقت الموعد المحدد (بداية الحضور)
                # effective_check_in_latest_dt.time() : نهاية الـ 10 دقائق بعد الموعد (نهاية التأخير)

                if effective_check_in_earliest_dt.time() <= entry_time_saudia <= start_time_obj:
                    status = FinalAttendanceStatus.PRESENT
                elif start_time_obj < entry_time_saudia <= effective_check_in_latest_dt.time():
                    status = FinalAttendanceStatus.LATE
                else:
                    # إذا كان وقت الدخول خارج نطاق الحضور أو التأخير المعرف (ولكنه لا يزال ضمن فترة التقرير العامة)،
                    # فسيتم التعامل معه هنا. افتراضياً، غائب عن هذه الفترة المحددة.
                    status = FinalAttendanceStatus.ABSENT
            
            # 🟢 البحث عن عذر موجود لهذا الطالب في هذا التاريخ
            existing_excuse = Excuse.query.filter(
                Excuse.student_id == student.id,
                Excuse.date_of_absence == report_date,
                Excuse.status == ExcuseStatus.APPROVED # فقط الأعذار الموافق عليها
            ).first()

            # إذا كان هناك عذر معتمد وحالته المحسوبة غائب (ABSENT)، يتم تغيير الحالة إلى EXCUSED
            if existing_excuse and status == FinalAttendanceStatus.ABSENT:
                status = FinalAttendanceStatus.EXCUSED 

            report_data.append({
                'student': student,
                'entry_time': entry_time_saudia.strftime('%H:%M') if entry_time_saudia else 'لا يوجد سجل',
                'calculated_status': status,
                'current_final_status': student_entry_log.final_status if student_entry_log and student_entry_log.final_status else FinalAttendanceStatus.UNKNOWN,
                'log_id': student_entry_log.id if student_entry_log else None, # ID للسجل لتحديثه لاحقًا
                'has_approved_excuse': existing_excuse is not None
            })

    return render_template('teacher/generate_report.html',
                           title='إنشاء تقرير الحضور',
                           form=form,
                           report_data=report_data,
                           report_date=report_date,
                           start_time=start_time_obj,
                           end_time=end_time_obj,
                           final_statuses=FinalAttendanceStatus)


@teacher_bp.route('/update_report_status', methods=['POST'])
@login_required
@teacher_required
def update_report_status():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'JSON request expected.'}), 400

    data = request.get_json()
    log_id = data.get('log_id')
    student_id = data.get('student_id')
    new_status_value = data.get('new_status')
    report_date_str = data.get('report_date')
    
    if not new_status_value:
        return jsonify({'success': False, 'message': 'New status is required.'}), 400

    try:
        new_status = FinalAttendanceStatus[new_status_value] # تحويل القيمة النصية إلى Enum
    except KeyError:
        return jsonify({'success': False, 'message': 'Invalid status value.'}), 400

    # إذا كان هناك log_id، فهذا يعني أن الطالب لديه سجل دخول
    if log_id:
        log = AttendanceLog.query.get(log_id)
        if log:
            log.final_status = new_status
            log.report_generated_at = datetime.now(pytz.utc)
            log.report_generated_by = current_user.id
            db.session.commit()
            return jsonify({'success': True, 'message': 'تم تحديث حالة الحضور للسجل بنجاح.'})
        else:
            return jsonify({'success': False, 'message': 'سجل الحضور غير موجود.'}), 404
    # إذا لم يكن هناك log_id، فهذا يعني أن الطالب لم يسجل دخولاً، ونريد تسجيل غيابه
    elif student_id and report_date_str:
        student = Student.query.get(student_id)
        report_date = datetime.strptime(report_date_str, '%Y-%m-%d').date()

        # نبحث عن AttendanceLog قديم تم إنشاؤه لهذا اليوم بواسطة المعلم
        # أو ننشئ واحدًا جديدًا إذا لم يكن موجودًا
        existing_log_for_report = AttendanceLog.query.filter(
            AttendanceLog.student_id == student_id,
            db.func.DATE(AttendanceLog.timestamp) == report_date,
            AttendanceLog.report_generated_by.isnot(None) # سجل تم إنشاؤه كتقرير
        ).first()

        if existing_log_for_report:
            existing_log_for_report.final_status = new_status
            existing_log_for_report.report_generated_at = datetime.now(pytz.utc)
            existing_log_for_report.report_generated_by = current_user.id
            db.session.commit()
            return jsonify({'success': True, 'message': 'تم تحديث حالة الحضور (تقرير) بنجاح.'})
        else:
            # إنشاء سجل حضور جديد من نوع 'تقرير' إذا لم يكن هناك سجل دخول فعلي
            # هذا ضروري لتخزين حالة الغياب أو الحضور بعذر عندما لا يكون هناك مسح بالبطاقة
            new_log = AttendanceLog(
                student_id=student_id,
                device_id=1, # 🟢 تحتاج لتحديد device_id افتراضي لـ "التقرير اليدوي" أو تعديل النموذج ليسمح بـ nullable
                timestamp=combine_date_time_to_saudia_tz(report_date, time(0,0,0)), # وقت في بداية اليوم
                status=AttendanceStatus.ENTER, # يمكن أن نضع حالة افتراضية أو ننشئ حالة جديدة مثل AttendanceStatus.REPORTED
                final_status=new_status,
                report_generated_at=datetime.now(pytz.utc),
                report_generated_by=current_user.id
            )
            db.session.add(new_log)
            db.session.commit()
            return jsonify({'success': True, 'message': 'تم إنشاء وتحديث حالة الحضور (تقرير) بنجاح.'})

    return jsonify({'success': False, 'message': 'Log ID أو Student ID وتاريخ التقرير مطلوبين.'}), 400


@teacher_bp.route('/finalize_report', methods=['POST'])
@login_required
@teacher_required
def finalize_report():
    if not request.is_json:
        return jsonify({'success': False, 'message': 'JSON request expected.'}), 400

    data = request.get_json()
    report_data_list = data.get('report_data')
    report_date_str = data.get('report_date')

    if not report_data_list or not report_date_str:
        return jsonify({'success': False, 'message': 'Report data and date are required.'}), 400

    report_date = datetime.strptime(report_date_str, '%Y-%m-%d').date()
    report_date_obj = report_date # اسم متغير أكثر وضوحًا إذا أردت استخدامه في الرسائل

    for entry in report_data_list:
        student_id = entry.get('student_id')
        final_status_value = entry.get('final_status')

        if not student_id or not final_status_value:
            continue

        try:
            final_status = FinalAttendanceStatus[final_status_value]
        except KeyError:
            continue # تجاهل الحالات غير الصالحة

        # 🟢🟢🟢 التعديل هنا لمعالجة مشكلة student_user 🟢🟢🟢
        student = Student.query.get(student_id)
        student_user = student.user_account if student and student.user_account else None
        # 🟢🟢🟢 انتهاء التعديل 🟢🟢🟢

        # البحث عن AttendanceLog لهذا الطالب في هذا اليوم
        # إما سجل دخول فعلي، أو سجل تقرير تم إنشاؤه مسبقًا
        # 🟢 البحث عن السجلات المتعلقة بهذا اليوم فقط لـ final_status
        log_to_update = AttendanceLog.query.filter(
            AttendanceLog.student_id == student_id,
            db.func.DATE(AttendanceLog.timestamp) == report_date
        ).order_by(AttendanceLog.timestamp.desc()).first() # نأخذ أحدث سجل لليوم

        if log_to_update:
            log_to_update.final_status = final_status
            log_to_update.report_generated_at = datetime.now(pytz.utc)
            log_to_update.report_generated_by = current_user.id
            db.session.add(log_to_update)
        else:
            # إذا لم يكن هناك سجل دخول أو سجل تقرير، ننشئ واحدًا جديدًا (خاصة للغياب)
            # 🟢 يجب أن يكون device_id هنا هو ID لجهاز افتراضي للتقارير أو يتم تعديل النموذج للسماح بـ nullable
            new_report_log = AttendanceLog(
                student_id=student_id,
                device_id=1, # 🟢 يجب أن يكون هذا رقم ID لجهاز افتراضي للتقارير أو يتم تعديل النموذج
                timestamp=combine_date_time_to_saudia_tz(report_date, time(0,0,0)), # وقت في بداية اليوم
                status=AttendanceStatus.ENTER, # حالة افتراضية، يمكن إضافة AttendanceStatus.REPORTED
                final_status=final_status,
                report_generated_at=datetime.now(pytz.utc),
                report_generated_by=current_user.id
            )
            db.session.add(new_report_log)

        # 🟢 إرسال إشعار للطالب إذا كان غائبًا أو متأخرًا (اختياري)
        # 🟢 تأكد من أن student_user موجود قبل محاولة إرسال إشعار
        if student_user and final_status in [FinalAttendanceStatus.ABSENT, FinalAttendanceStatus.LATE, FinalAttendanceStatus.EXCUSED]:
            notification_message = f"تم تحديث حالة حضورك بتاريخ {report_date_obj.strftime('%Y-%m-%d')} إلى '{final_status.value}'."
            new_notification = Notification(
                sender_id=current_user.id,
                receiver_id=student_user.id,
                message=notification_message,
                status='unread',
                type='attendance_update'
            )
            db.session.add(new_notification)

    try:
        db.session.commit()
        flash('تم تعميم تقرير الحضور بنجاح!', 'success')
        return jsonify({'success': True, 'message': 'Report finalized successfully!'})
    except Exception as e:
        db.session.rollback()
        print(f"Error in finalize_report: {e}") # 🟢 طباعة الخطأ لتسهيل التصحيح
        return jsonify({'success': False, 'message': f'حدث خطأ أثناء تعميم التقرير: {str(e)}'}), 500