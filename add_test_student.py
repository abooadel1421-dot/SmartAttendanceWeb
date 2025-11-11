# add_test_student.py  

import os  
import sys  

# أضف مسار المجلد الأب (حيث يوجد مجلد 'app') إلى PYTHONPATH  
# هذا يضمن أن الاستيرادات مثل 'from app import create_app' تعمل بشكل صحيح  
current_dir = os.path.dirname(os.path.abspath(__file__))  
parent_dir = os.path.join(current_dir, '..')  

sys.path.insert(0, parent_dir)  


from app import create_app, db  
from app.models.user import User, UserRole  
from app.models.student import Student  
from app.models.card import Card  
from app.models.attendance_log import AttendanceLog  
from datetime import datetime, date  
from werkzeug.security import generate_password_hash  

def add_test_student_data():  
    app = create_app()  
    with app.app_context():  
        print("بدء إضافة بيانات الطالب التجريبي...")  

        # ----------------------------------------------------  
        # 1. تعريف بيانات الطالب التجريبي  
        # ----------------------------------------------------  
        student_username = 'student_test'  
        student_email = 'student_test@example.com'  
        student_password = 'password123'  
        student_id_number = 'S2023001'  

        # ----------------------------------------------------  
        # 2. إنشاء حساب المستخدم (User)  
        # ----------------------------------------------------  
        user = User.query.filter_by(username=student_username).first()  
        if user:  
            print(f"المستخدم '{student_username}' موجود بالفعل. تحديث كلمة المرور والدور إذا لزم الأمر.")  
            user.set_password(student_password)  
            user.role = UserRole.STUDENT  
        else:  
            user = User(username=student_username, email=student_email, role=UserRole.STUDENT)  
            user.set_password(student_password)  
            db.session.add(user)  
            print(f"تم إنشاء حساب المستخدم: {student_username}")  
        # commit هنا لحفظ الـ user_id قبل استخدامه  
        db.session.commit()  

        # ----------------------------------------------------  
        # 3. إنشاء بيانات الطالب (Student)  
        # ----------------------------------------------------  
        # البحث عن الطالب باستخدام user_id  
        student_data = Student.query.filter_by(user_id=user.id).first()  
        if student_data:  
            print(f"بيانات الطالب لـ '{user.username}' موجودة بالفعل. تحديث البيانات.")  
            student_data.student_id_number = student_id_number  
            student_data.first_name = 'سارة'  
            student_data.last_name = 'محمد'  
            student_data.parent_email = 'parent.sara@example.com'  
            student_data.parent_phone_number = '0501234567'  
            student_data.major = 'هندسة برمجيات'  
            student_data.grade = 'ثانية جامعي'  
            student_data.date_of_birth = date(2002, 10, 20)  
            student_data.is_active = True  
            # تأكد من أن student_data.user_id لا يزال صحيحًا  
            student_data.user_id = user.id  
        else:  
            student_data = Student(  
                user_id=user.id, # ربط الطالب بالمستخدم  
                student_id_number=student_id_number,  
                first_name='سارة',  
                last_name='محمد',  
                parent_email='parent.sara@example.com',  
                parent_phone_number='0501234567',  
                major='هندسة برمجيات',  
                grade='ثانية جامعي',  
                date_of_birth=date(2002, 10, 20),  
                is_active=True  
            )  
            db.session.add(student_data)  
            print(f"تم إنشاء بيانات الطالب لـ: {student_data.first_name} {student_data.last_name}")  
        # commit هنا لحفظ الـ student_data.id قبل استخدامه لربط المستخدم بالطالب  
        db.session.commit()  

        # ----------------------------------------------------  
        # 4. تحديث user.student_id لربط المستخدم بملف الطالب  
        # ----------------------------------------------------  
        # هذا يضمن أن العلاقة من جانب User إلى Student مكتملة.  
        # SQLAlchemy قد يدير هذا تلقائيًا، لكن التعيين الصريح يضمن ذلك.  
        if user.student_id != student_data.id:  
            user.student_id = student_data.id  
            db.session.add(user) # أضف المستخدم مرة أخرى لتحديثه  
            print(f"تم ربط المستخدم '{user.username}' بالطالب '{student_data.full_name}'.")  
            db.session.commit() # commit لتحديث user.student_id  


        # ----------------------------------------------------  
        # 5. (اختياري) إنشاء بطاقة (Card) للطالب  
        # ----------------------------------------------------  
        card_uid = 'NFC123456789'  
        card = Card.query.filter_by(student_id=student_data.id).first()  
        if card:  
            print(f"البطاقة لـ '{student_data.full_name}' موجودة بالفعل. تحديث بيانات البطاقة.")  
            card.card_uid = card_uid  
            card.status = 'ACTIVE'  
        else:  
            card = Card(  
                student_id=student_data.id,  
                card_uid=card_uid,  
                issued_at=datetime.utcnow(),  
                status='ACTIVE'  
            )  
            db.session.add(card)  
            print(f"تم إنشاء بطاقة لـ: {student_data.full_name}")  
        db.session.commit()  

        # ----------------------------------------------------  
        # 6. (اختياري) إضافة سجلات حضور تجريبية  
        # ----------------------------------------------------  
        # ... (الجزء الخاص بسجلات الحضور كما هو في كودك الأصلي) ...  

        print("\n----------------------------------------------------")  
        print(f"تمت إضافة/تحديث بيانات الطالب التجريبي بنجاح.")  
        print(f"اسم المستخدم: {student_username}")  
        print(f"كلمة المرور: {student_password}")  
        print(f"الرقم الجامعي: {student_id_number}")  
        print("----------------------------------------------------")  

if __name__ == '__main__':  
    add_test_student_data()