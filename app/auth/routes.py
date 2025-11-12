from flask import render_template, redirect, url_for, flash, request  
from flask_login import current_user, login_user, logout_user, login_required  
from .. import db  
from app.auth import bp as auth_bp  
from app.auth.forms import LoginForm, RegistrationForm  
from app.models.user import User, UserRole  

@auth_bp.route('/login', methods=['GET', 'POST'])  
@auth_bp.route('/login/<string:role_param>', methods=['GET', 'POST'])  
def login(role_param=None):  
    requested_role = role_param if role_param else request.args.get('role')  
    print(f"DEBUG AUTH: Accessing login route. Requested role: {requested_role}")  

    if current_user.is_authenticated:  
        print(f"DEBUG AUTH: User already authenticated. Username: {current_user.username}, Role: {current_user.role}")  
        if current_user.role == UserRole.ADMIN:  
            print("DEBUG AUTH: Redirecting authenticated admin to admin.index")  
            return redirect(url_for('admin.index'))  
        elif current_user.role == UserRole.TEACHER:  
            print("DEBUG AUTH: Redirecting authenticated teacher to teacher.dashboard")  
            return redirect(url_for('teacher.dashboard'))  
        elif current_user.role == UserRole.STUDENT:  
            print("DEBUG AUTH: Redirecting authenticated student to student.dashboard")  
            return redirect('/student/dashboard')  # ✅ تغيير هنا
        else:  
            print("DEBUG AUTH: Authenticated user with unknown role. Redirecting to main.index")  
            flash('دور المستخدم الحالي غير معروف، يرجى الاتصال بالدعم.', 'warning')  
            return redirect(url_for('main.index'))  

    form = LoginForm()  
    if form.validate_on_submit():  
        user = User.query.filter_by(username=form.username.data).first()  
        print(f"DEBUG AUTH: Login form submitted. Username: {form.username.data}")  

        if user is None or not user.check_password(form.password.data):  
            print(f"DEBUG AUTH: Login failed for username: {form.username.data}")  
            flash('اسم مستخدم أو كلمة مرور غير صحيحة.', 'danger')  
            return redirect(url_for('auth_bp.login', role=requested_role))  

        print(f"DEBUG AUTH: User found: {user.username}, Actual Role: {user.role}")  

        if requested_role and user.role.value != requested_role:  
            print(f"DEBUG AUTH: Role mismatch. User's actual role '{user.role.value}' does not match requested role '{requested_role}'.")  
            flash(f'لا يمكنك تسجيل الدخول كـ "{requested_role}". حسابك هو "{user.role.value}".', 'danger')  
            return redirect(url_for('auth_bp.login', role=requested_role))  

        login_user(user, remember=form.remember_me.data)  
        flash(f'مرحباً بعودتك، {user.username}!', 'success')  
        print(f"DEBUG AUTH: User '{user.username}' logged in successfully.")  

        next_page = request.args.get('next')  
        if next_page and next_page.startswith('/'):  
            print(f"DEBUG AUTH: Redirecting to 'next_page': {next_page}")  
            return redirect(next_page)  
# ...

        else:  
            if user.role == UserRole.ADMIN:  
                print("DEBUG AUTH: Post-login redirecting admin to admin.index")  
                # تأكد أن اسم الـ Blueprint للأدمن هو 'admin'
                return redirect(url_for('admin.index'))  
            elif user.role == UserRole.TEACHER:  
                print("DEBUG AUTH: Post-login redirecting teacher to teacher.dashboard")  
                # ✅ التغيير هنا: استخدم اسم الـ Blueprint 'teacher'
                return redirect(url_for('teacher.dashboard'))  
            elif user.role == UserRole.STUDENT:  
                print("DEBUG AUTH: Post-login redirecting student to student.dashboard")  
                # ✅ التغيير هنا: استخدم url_for بدلاً من المسار الثابت
                # تأكد أن اسم الـ Blueprint للطالب هو 'student'
                return redirect(url_for('student.dashboard'))  
            else:  
                print("DEBUG AUTH: Post-login user with unknown role. Redirecting to main.index")  
                flash('دور المستخدم غير معروف بعد تسجيل الدخول.', 'warning')  
                return redirect(url_for('main.index'))  

# ...

    print("DEBUG AUTH: Rendering login form (GET request).")  
    return render_template('auth/login.html', title='تسجيل الدخول', form=form, requested_role=requested_role)  

@auth_bp.route('/logout')  
@login_required  
def logout():  
    logout_user()  
    flash('تم تسجيل خروجك بنجاح.', 'info')  
    return redirect(url_for('main.index'))  

@auth_bp.route('/register', methods=['GET', 'POST'])  
def register():  
    if current_user.is_authenticated:  
        return redirect(url_for('main.index'))  

    form = RegistrationForm()  
    if form.validate_on_submit():  
        user = User(  
            username=form.username.data,  
            email=form.email.data,  
            role=UserRole.STUDENT  
        )  
        user.set_password(form.password.data)  
        db.session.add(user)  
        db.session.commit()  
        flash('تهانينا، تم تسجيلك كمستخدم جديد!', 'success')  
        return redirect(url_for('auth_bp.login'))  
    return render_template('auth/register.html', title='تسجيل حساب جديد', form=form)