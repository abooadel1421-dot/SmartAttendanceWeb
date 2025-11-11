from flask import render_template, flash, redirect, url_for, request  
from app.students import bp  
from app.students.forms import StudentForm  
from app.models.student import Student  
from .. import db  
from flask_login import login_required, current_user  
from app.utils.permissions import permission_required, Role  

# مسار لعرض قائمة الطلاب  
# سيصبح المسار الفعلي: /students/  
@bp.route('/')  
@bp.route('/index') # يمكنك إضافة هذا المسار أيضاً إذا أردت /students/index  
@login_required  
# @permission_required(Role.ADMIN)  
def index():  
    page = request.args.get('page', 1, type=int)  
    students_pagination = Student.query.order_by(Student.last_name.asc()).paginate(  
        page=page, per_page=10, error_out=False)  

    next_url = url_for('students.index', page=students_pagination.next_num) if students_pagination.has_next else None  
    prev_url = url_for('students.index', page=students_pagination.prev_num) if students_pagination.has_prev else None  

    return render_template('students/index.html', title='إدارة الطلاب',  
                           students=students_pagination.items,  
                           next_url=next_url, prev_url=prev_url,  
                           pagination=students_pagination)  

# مسار لإضافة طالب جديد  
# سيصبح المسار الفعلي: /students/add  
@bp.route('/add', methods=['GET', 'POST']) # ❌ تم تعديل هذا السطر  
@login_required  
# @permission_required(Role.ADMIN)  
def add_student():  
    form = StudentForm()  
    if form.validate_on_submit():  
        student = Student(  
            student_id_number=form.student_id_number.data,  
            first_name=form.first_name.data,  
            last_name=form.last_name.data,  
            email=form.email.data,  
            phone_number=form.phone_number.data,  
            grade=form.grade.data,  
            major=form.major.data,  
            date_of_birth=form.date_of_birth.data,  
            is_active=form.is_active.data  
        )  
        db.session.add(student)  
        db.session.commit()  
        flash('تمت إضافة الطالب بنجاح!', 'success')  
        return redirect(url_for('students.index'))  
    return render_template('students/add_edit.html', title='إضافة طالب جديد', form=form, is_edit=False)  

# مسار لتعديل بيانات طالب  
# سيصبح المسار الفعلي: /students/edit/<int:id>  
@bp.route('/edit/<int:id>', methods=['GET', 'POST']) # ❌ تم تعديل هذا السطر  
@login_required  
@permission_required(Role.ADMIN)  
def edit_student(id):  
    student = Student.query.get_or_404(id)  
    form = StudentForm(original_id_number=student.student_id_number, original_email=student.email)  
    if form.validate_on_submit():  
        student.student_id_number = form.student_id_number.data  
        student.first_name = form.first_name.data  
        student.last_name = form.last_name.data  
        student.email = form.email.data  
        student.phone_number = form.phone_number.data  
        student.grade = form.grade.data  
        student.major = form.major.data  
        student.date_of_birth = form.date_of_birth.data  
        student.is_active = form.is_active.data  
        db.session.commit()  
        flash('تم تحديث بيانات الطالب بنجاح!', 'success')  
        return redirect(url_for('students.index'))  
    elif request.method == 'GET':  
        form.student_id_number.data = student.student_id_number  
        form.first_name.data = student.first_name  
        form.last_name.data = student.last_name  
        form.email.data = student.email  
        form.phone_number.data = student.phone_number  
        form.grade.data = student.grade  
        form.major.data = student.major  
        form.date_of_birth.data = student.date_of_birth  
        form.is_active.data = student.is_active  
    return render_template('students/add_edit.html', title='تعديل طالب', form=form, is_edit=True, student_id=student.id)  

# مسار لعرض تفاصيل طالب  
# سيصبح المسار الفعلي: /students/<int:id>  
@bp.route('/<int:id>') # ❌ تم تعديل هذا السطر  
@login_required  
@permission_required(Role.ADMIN)  
def view_student(id):  
    student = Student.query.get_or_404(id)  
    return render_template('students/view_student.html', title='تفاصيل الطالب', student=student)  

# مسار لحذف طالب  
# سيصبح المسار الفعلي: /students/delete/<int:id>  
@bp.route('/delete/<int:id>', methods=['POST']) # ❌ تم تعديل هذا السطر  
@login_required  
@permission_required(Role.ADMIN)  
def delete_student(id):  
    student = Student.query.get_or_404(id)  

    if student.card.first():  
        flash('لا يمكن حذف الطالب لديه بطاقة NFC مرتبطة. يرجى حذف البطاقة أولاً.', 'danger')  
        return redirect(url_for('students.index'))  

    if student.attendance_records.first():  
        flash('لا يمكن حذف الطالب لديه سجلات حضور مرتبطة. يرجى حذف السجلات أولاً.', 'danger')  
        return redirect(url_for('students.index'))  

    try:  
        db.session.delete(student)  
        db.session.commit()  
        flash('تم حذف الطالب بنجاح!', 'success')  
    except Exception as e:  
        db.session.rollback()  
        flash(f'حدث خطأ أثناء حذف الطالب: {str(e)}', 'danger')  
    return redirect(url_for('students.index'))