# app/services/data_processing.py  

from datetime import datetime, timedelta  
from .. import db  
from app.models.attendance_log import AttendanceLog, AttendanceStatus # تحتاج لتعريف هذا النموذج  
from app.models.student import Student  
from app.models.card import NFCCard # نموذج بطاقة NFC  

class DataProcessingService:  
    """  
    خدمة لمعالجة وتخزين بيانات الحضور.  
    """  

    def process_attendance_record(self, nfc_id: str, device_id: str, timestamp: datetime = None) -> dict:  
        """  
        يقوم بتسجيل أو تحديث سجل الحضور بناءً على بيانات NFC.  

        Args:  
            nfc_id (str): معرف بطاقة NFC الفريد.  
            device_id (str): معرف الجهاز الذي قام بالقراءة.  
            timestamp (datetime, optional): وقت القراءة. إذا لم يتم توفيره، سيتم استخدام الوقت الحالي.  

        Returns:  
            dict: قاموس يحتوي على نتيجة العملية (نجاح/فشل، رسالة، بيانات السجل).  
        """  
        if timestamp is None:  
            timestamp = datetime.utcnow()  

        # 1. البحث عن البطاقة والطالب المرتبط بها  
        card = NFCCard.query.filter_by(nfc_uid=nfc_id).first()  
        if not card:  
            return {"status": "error", "message": f"بطاقة NFC بمعرف {nfc_id} غير مسجلة."}  
        
        student = Student.query.get(card.student_id)  
        if not student:  
            return {"status": "error", "message": f"لا يوجد طالب مرتبط ببطاقة {nfc_id}."}  

        # 2. التحقق من التكرار أو تسجيل الدخول/الخروج المزدوج في فترة قصيرة  
        #    مثال: لا تسجل حركة أخرى لنفس الطالب من نفس الجهاز خلال دقيقة واحدة  
        last_log = AttendanceLog.query.filter_by(  
            student_id=student.id,  
            device_id=device_id  
        ).order_by(AttendanceLog.timestamp.desc()).first()  

        if last_log and (timestamp - last_log.timestamp) < timedelta(minutes=1):  
            return {"status": "warning", "message": "تم تسجيل حركة لهذا الطالب مؤخرًا من نفس الجهاز."}  

        # 3. تحديد نوع الحركة (دخول/خروج) أو حالة الحضور  
        #    هنا يمكنك تطبيق منطق معقد:  
        #    - إذا كانت هذه هي أول حركة لهذا الطالب في اليوم: تسجيل دخول  
        #    - إذا كانت آخر حركة هي دخول: تسجيل خروج  
        #    - إذا كان النظام يسجل فقط "الحضور" بغض النظر عن الدخول/الخروج: مجرد تسجيل دخول  
        
        # لنفترض هنا أن كل قراءة هي "حضور" مبدئياً،  
        # ويمكن توسيعها لتحديد ENTRANCE / EXIT لاحقاً  
        
        # سجل جديد  
        new_log = AttendanceLog(  
            student_id=student.id,  
            device_id=device_id,  
            timestamp=timestamp,  
            status=AttendanceStatus.PRESENT # افتراضي، يمكن أن يكون DURATION, ENTRANCE, EXIT  
        )  
        db.session.add(new_log)  
        db.session.commit()  

        return {  
            "status": "success",  
            "message": f"تم تسجيل حضور الطالب {student.full_name}.",  
            "log": {  
                "id": new_log.id,  
                "student_id": student.id,  
                "student_name": student.full_name,  
                "device_id": device_id,  
                "timestamp": new_log.timestamp.isoformat(),  
                "status": new_log.status.value  
            }  
        }  
    
    def get_daily_attendance_summary(self, date: datetime = None) -> list[dict]:  
        """  
        يحسب ملخص الحضور اليومي.  
        مثلاً: عدد الحاضرين، الغائبين، إجمالي الطلاب.  
        """  
        if date is None:  
            date = datetime.utcnow().date()  
        
        start_of_day = datetime(date.year, date.month, date.day)  
        end_of_day = start_of_day + timedelta(days=1)  

        total_students = Student.query.count()  
        present_students_ids = set(  
            db.session.query(AttendanceLog.student_id)  
            .filter(AttendanceLog.timestamp >= start_of_day, AttendanceLog.timestamp < end_of_day)  
            .group_by(AttendanceLog.student_id)  
            .all()  
        )  
        
        present_count = len(present_students_ids)  
        absent_count = total_students - present_count  

        return {  
            "date": date.isoformat(),  
            "total_students": total_students,  
            "present_students": present_count,  
            "absent_students": absent_count,  
            "details_available": url_for('attendance.daily_details', date=date.isoformat()) # مثال لإنشاء رابط  
        }  


# ملاحظات:  
# - يجب أن تقوم بتعريف نماذج AttendanceLog و AttendanceStatus و Student و NFCCard في app/models.  
# - يمكن إضافة وظائف أخرى هنا مثل حساب مدة الحضور، تنظيف البيانات غير الصحيحة، إلخ.