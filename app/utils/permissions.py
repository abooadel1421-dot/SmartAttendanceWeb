from functools import wraps  
from flask import abort, flash, redirect, url_for  
from flask_login import current_user  
import enum  

class Role(enum.Enum):  
    ADMIN = 'ADMIN'  
    TEACHER = 'TEACHER'  
    STUDENT = 'STUDENT'  

    def __str__(self):  
        return self.value  

def permission_required(role):  
    def decorator(f):  
        @wraps(f)  
        def decorated_function(*args, **kwargs):  
            if not current_user.is_authenticated:  
                flash('يرجى تسجيل الدخول للوصول إلى هذه الصفحة.', 'warning')  
                return redirect(url_for('auth_bp.login'))  
            
            # نفترض أن نموذج المستخدم لديه حقل 'role' من نوع Role Enum  
            # تأكد أن current_user.role هو كائن من نوع Role Enum  
            if not isinstance(current_user.role, Role) or current_user.role != role:  
                flash('ليس لديك الصلاحيات اللازمة للوصول إلى هذه الصفحة.', 'danger')  
                abort(403) # أو توجيه لصفحة خطأ 403 مخصصة  
            return f(*args, **kwargs)  
        return decorated_function  
    return decorator