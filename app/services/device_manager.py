# app/services/device_manager.py  

from .. import db # تأكد من أن db متاح  
from app.models.device import Device # نموذج الجهاز الذي قمت بتحديده  

class DeviceManagerService:  
    """  
    خدمة لإدارة أجهزة قارئ NFC (ESP32).  
    """  

    def get_all_devices(self) -> list[Device]:  
        """يعيد قائمة بجميع الأجهزة المسجلة."""  
        return Device.query.all()  

    def get_device_by_id(self, device_id: int) -> Device | None:  
        """يعيد جهازاً معيناً بواسطة ID."""  
        return Device.query.get(device_id)  

    def get_device_by_serial(self, serial_number: str) -> Device | None:  
        """يعيد جهازاً بواسطة رقمه التسلسلي."""  
        return Device.query.filter_by(serial_number=serial_number).first()  

    def add_device(self, serial_number: str, location: str, description: str = None) -> Device:  
        """يضيف جهازاً جديداً."""  
        if self.get_device_by_serial(serial_number):  
            raise ValueError(f"الجهاز بالرقم التسلسلي {serial_number} موجود بالفعل.")  
        
        new_device = Device(serial_number=serial_number, location=location, description=description)  
        db.session.add(new_device)  
        db.session.commit()  
        return new_device  

    def update_device(self, device_id: int, serial_number: str = None, location: str = None, description: str = None, is_active: bool = None) -> Device | None:  
        """يحدث معلومات جهاز موجود."""  
        device = self.get_device_by_id(device_id)  
        if not device:  
            raise ValueError(f"الجهاز بالـ ID {device_id} غير موجود.")  
        
        if serial_number:  
            device.serial_number = serial_number  
        if location:  
            device.location = location  
        if description is not None:  
            device.description = description  
        if is_active is not None:  
            device.is_active = is_active  
            
        db.session.commit()  
        return device  

    def delete_device(self, device_id: int) -> bool:  
        """يحذف جهازاً."""  
        device = self.get_device_by_id(device_id)  
        if device:  
            db.session.delete(device)  
            db.session.commit()  
            return True  
        return False  

    def activate_device(self, device_id: int) -> Device | None:  
        """ينشط جهازاً."""  
        return self.update_device(device_id, is_active=True)  

    def deactivate_device(self, device_id: int) -> Device | None:  
        """يعطل جهازاً."""  
        return self.update_device(device_id, is_active=False)  

# مثال على كيفية استخدامه (لن يتم تشغيله مباشرة هنا)  
if __name__ == '__main__':  
    # هذا يتطلب تهيئة Flask و SQLAlchemy للعمل  
    # من الأفضل اختبار هذه الخدمات من خلال الاختبارات الوحدة أو ضمن سياق Flask  
    pass