# add_data.py  
from app import create_app, db  
from app.models import Device, Student, Card # استورد كل النماذج التي تحتاجها  
from datetime import datetime, date # استورد date أيضًا لـ date_of_birth  
import uuid  
import pytz # استورد pytz  

app = create_app()  
with app.app_context():  
    print("Adding initial data...")  

    # 1. إضافة الجهاز (Device)  
    device_sn = "ESP32_LAB_001"  
    existing_device = Device.query.filter_by(serial_number=device_sn).first()  
    if not existing_device:  
        # استخدام datetime.now(datetime.UTC) بدلاً من utcnow() لتجنب التحذير  
        new_device = Device(serial_number=device_sn, name="Entrance Gate Reader", location="Main Entrance", status="active", last_seen=pytz.utc.localize(datetime.utcnow())) 
        db.session.add(new_device)  
        print(f"Device '{device_sn}' added.")  
    else:  
        print(f"Device '{device_sn}' already exists.")  
    
    # 2. إضافة طالب (Student)  
    student_id_number = "BAU2025001" # رقم تعريف الطالب (يمكن أن يكون عشوائيًا أو يدويًا)  
    existing_student = Student.query.filter_by(student_id_number=student_id_number).first()  
    if not existing_student:  
        new_student = Student(  
            first_name="Ahmed",  
            last_name="Ali",  
            student_id_number=student_id_number,  
            # استخدم parent_email بدلاً من email  
            parent_email=f"ahmed.parent@{uuid.uuid4().hex[:4]}.com",   
            # استخدم grade بدلاً من level  
            grade="12th Grade",   
            major="Computer Science",  
            # استخدم parent_phone_number بدلاً من phone_number  
            parent_phone_number="0501234567",  
            date_of_birth=date(2005, 5, 15) # مثال لتاريخ الميلاد  
        )  
        db.session.add(new_student)  
        db.session.commit() # commit هنا للحصول على ID للطالب  
        print(f"Student '{new_student.full_name}' added.")  
        student_to_use = new_student  
    else:  
        print(f"Student '{existing_student.full_name}' already exists.")  
        student_to_use = existing_student  
    
    # 3. إضافة بطاقة (Card) وربطها بالطالب  
    card_uid_to_add = "1D0B65E00B1080" # استخدم الـ UID الفعلي لبطاقتك  
    existing_card = Card.query.filter_by(card_uid=card_uid_to_add).first()  
    if not existing_card:  
        if student_to_use:  
            new_card = Card(card_uid=card_uid_to_add, student_id=student_to_use.id, status="active")  
            db.session.add(new_card)  
            print(f"Card '{card_uid_to_add}' linked to student '{student_to_use.full_name}'.")  
        else:  
            print(f"Error: No student available to link card '{card_uid_to_add}'.")  
    else:  
        print(f"Card '{card_uid_to_add}' already exists and is linked to student '{existing_card.student.full_name}'.")  

    db.session.commit() # تأكيد جميع التغييرات المتبقية  
    print("Initial data script finished.")