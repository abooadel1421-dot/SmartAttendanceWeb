# app/services/nfc_reader.py  

import json  
# قد تحتاج لاستيراد وحدات من app.models لتتعامل مع البطاقات أو الطلاب  
# من app.models.card import NFCCard  
# من app.models.student import Student  

class NFCReaderService:  
    """  
    خدمة لمعالجة البيانات الواردة من قارئ NFC (ESP32).  
    """  

    def __init__(self):  
        # يمكن تهيئة أي اتصال أو إعدادات هنا إذا لزم الأمر  
        pass  

    def process_nfc_data(self, nfc_id: str, device_id: str, timestamp: str = None) -> dict:  
        """  
        تعالج بيانات NFC المستلمة من جهاز ESP32.  

        Args:  
            nfc_id (str): معرف بطاقة NFC الفريد.  
            device_id (str): معرف الجهاز الذي قام بالقراءة (ESP32).  
            timestamp (str, optional): وقت القراءة. إذا لم يتم توفيره، سيتم استخدام الوقت الحالي.  

        Returns:  
            dict: قاموس يحتوي على نتيجة المعالجة (نجاح/فشل، رسالة، بيانات الطالب إن وجدت).  
        """  
        # 1. التحقق من صحة البيانات الأساسية  
        if not nfc_id or not device_id:  
            return {"status": "error", "message": "بيانات NFC غير كاملة."}  

        # 2. البحث عن البطاقة في قاعدة البيانات  
        # card = NFCCard.query.filter_by(nfc_uid=nfc_id).first()  
        # if not card:  
        #     return {"status": "error", "message": f"بطاقة NFC بمعرف {nfc_id} غير مسجلة."}  

        # 3. ربط البطاقة بطالب  
        # student = Student.query.get(card.student_id) # بافتراض وجود علاقة  
        # if not student:  
        #     return {"status": "error", "message": f"لا يوجد طالب مرتبط ببطاقة {nfc_id}."}  

        # 4. تمرير البيانات لوحدة معالجة الحضور (attendance/routes.py أو data_processing.py)  
        #    هذه الخطوة عادة ما تتم في الـ Blueprint أو في خدمة أخرى  
        #    هنا، نفترض أن هذه الخدمة فقط تجهز البيانات  

        # مثال افتراضي للعودة  
        processed_data = {  
            "status": "success",  
            "message": "تم معالجة بيانات NFC بنجاح (للتسجيل).",  
            "nfc_id": nfc_id,  
            "device_id": device_id,  
            "timestamp": timestamp, # أو datetime.utcnow() إذا تم إنشاؤه هنا  
            # "student_id": student.id,  
            # "student_name": student.full_name  
        }  
        return processed_data  

    def handle_incoming_request(self, request_data: dict) -> dict:  
        """  
        واجهة عامة لمعالجة طلب وارد من جهاز ESP32 (سواء HTTP POST أو WebSocket).  

        Args:  
            request_data (dict): البيانات المستلمة من ESP32. يجب أن تحتوي على 'nfc_id' و 'device_id'.  

        Returns:  
            dict: قاموس يحتوي على نتيجة المعالجة.  
        """  
        nfc_id = request_data.get('nfc_id')  
        device_id = request_data.get('device_id')  
        timestamp = request_data.get('timestamp') # ESP32 قد يرسل وقتاً  

        return self.process_nfc_data(nfc_id, device_id, timestamp)  

# مثال على كيفية استخدامه (لن يتم تشغيله مباشرة هنا)  
if __name__ == '__main__':  
    nfc_service = NFCReaderService()  
    # بيانات مثال من ESP32  
    sample_data = {  
        "nfc_id": "ABCDEF123456",  
        "device_id": "ESP32-001",  
        "timestamp": "2023-10-27T10:30:00Z"  
    }  
    result = nfc_service.handle_incoming_request(sample_data)  
    print(result)