# create_admin.py
from app import create_app, db  
from werkzeug.security import generate_password_hash  
import os  

app = create_app()  

with app.app_context():  
    # ----------------------------------------------------
    # استيراد النماذج هنا، داخل سياق التطبيق أو بعد تهيئة db
    from app.models.user import User, UserRole # استيراد UserRole
    # لا حاجة لاستيراد Device هنا إذا تم استيراده بالفعل في app/__init__.py
    # ----------------------------------------------------

    admin_exists = User.query.filter_by(username='admin').first()  
    if admin_exists:  
        print("حساب المدير موجود بالفعل.")  
    else:  
        admin_user = User(  
            username='admin',  
            email='admin@example.com',  
            password_hash=generate_password_hash('AdminSecurePassword123'),  
            role=UserRole.ADMIN  
        )  
        db.session.add(admin_user)  
        db.session.commit()  
        print("تم إنشاء حساب المدير بنجاح: المستخدم 'admin' بكلمة المرور 'AdminSecurePassword123'")  

    print("\nقائمة المستخدمين الحاليين:")  
    users = User.query.all()  
    for user in users:  
        # تأكد من أن is_active موجود إذا كنت تستخدمه
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role.value if user.role else 'N/A'}") 