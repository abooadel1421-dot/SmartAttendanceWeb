# app/models/device.py  
from .. import db  
from datetime import datetime  
import enum  
import pytz # استيراد pytz  
from .. import db # <--- يجب أن يكون هكذا  

# تعريف DeviceStatus  
class DeviceStatus(enum.Enum):  
    ONLINE = "online"  
    OFFLINE = "offline"  
    DISABLED = "disabled"  
    ERROR = "error"  
    MAINTENANCE = "maintenance"  

class Device(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  

    serial_number = db.Column(db.String(50), unique=True, nullable=False, index=True)  
    name = db.Column(db.String(100), nullable=False)  

    location = db.Column(db.String(100), nullable=False)  

    # تحديث datetime.utcnow  
    added_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))  
    last_seen = db.Column(db.DateTime, nullable=True)  

    status = db.Column(db.Enum(DeviceStatus), default=DeviceStatus.OFFLINE, nullable=False)  

    # المفتاح الأجنبي  
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  

    # علاقات (Relationships) مع نماذج أخرى  
    # 'manager' في Device تقابل 'managed_devices' في User  
    manager = db.relationship('User', back_populates='managed_devices')  

    # علاقة مع AttendanceLog  
    # 'attendance_logs' في Device تقابل 'device' في AttendanceLog  
    attendance_logs = db.relationship('AttendanceLog', back_populates='device', lazy='dynamic')  


    def __repr__(self):  
        return f'<Device {self.name} (SN: {self.serial_number}) - Status: {self.status.value}>'