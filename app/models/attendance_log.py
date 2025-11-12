# app/models/attendance_log.py

from app import db
from datetime import datetime
import enum
import pytz

# 🟢 إضافة حالات جديدة للحضور والغياب النهائية
class FinalAttendanceStatus(enum.Enum):
    PRESENT = "حاضر"
    LATE = "متأخر"
    ABSENT = "غائب"
    EXCUSED = "غائب بعذر" # <--- غيّر EXCUSED_ABSENCE إلى EXCUSED
    UNKNOWN = "غير معروف"
    
class AttendanceStatus(enum.Enum):
    ENTER = "دخول"
    EXIT = "خروج"
    # يمكن أن تحتوي على حالات أخرى مثل LATE_ENTER إذا كان الجهاز يدعمها، لكننا سنعتمد على حساب الاعظاء هيئة التدريس.


class AttendanceLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='SET NULL'), nullable=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))
    status = db.Column(db.Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.ENTER)
    
    card_id = db.Column(db.Integer, db.ForeignKey('card.id', ondelete='SET NULL'), nullable=True)
    
    final_status = db.Column(db.Enum(FinalAttendanceStatus), nullable=True) # سيتم تعيينها بواسطة الاعظاء هيئة التدريس
    report_generated_at = db.Column(db.DateTime, nullable=True) # متى تم إنشاء/تحديث التقرير
    report_generated_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # الاعظاء هيئة التدريس الذي أنشأ التقرير

    # علاقات
    student = db.relationship('Student', back_populates='attendance_records')
    device = db.relationship('Device', back_populates='attendance_logs')
    reporter = db.relationship('User', foreign_keys=[report_generated_by]) # علاقة للمستخدم الذي أنشأ التقرير
    card = db.relationship('Card', back_populates='attendance_logs')

    def __repr__(self):
        return f'<AttendanceLog {self.student.full_name} - {self.status.value} at {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}>'
