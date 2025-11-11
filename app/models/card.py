# app/models/card.py  
from .. import db  
from datetime import datetime  
import enum  
import pytz  

# تعريف CardStatus  
class CardStatus(enum.Enum):  
    ACTIVE = "active"  
    INACTIVE = "inactive"  
    LOST = "lost"  
    DAMAGED = "damaged"  

class Card(db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    card_uid = db.Column(db.String(50), unique=True, nullable=False, index=True)  
    issued_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))  
    expires_at = db.Column(db.DateTime, nullable=True)  
    status = db.Column(db.Enum(CardStatus), default=CardStatus.ACTIVE, nullable=False)  

    # ***** التعديل هنا: student_id يصبح nullable=True *****  
    # يبقى unique=True لأن الطالب الواحد يمتلك بطاقة واحدة فقط  
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), unique=True, nullable=True, index=True)  

    # تحديث العلاقة لاستخدام back_populates  
    # 'student' هو اسم الخاصية في نموذج Student التي تشير إلى Card (وهي 'card')  
    student = db.relationship('Student', back_populates='card')  

    # علاقة مع AttendanceLog  
    attendance_logs = db.relationship('AttendanceLog', back_populates='card', lazy='dynamic')  

    def __repr__(self):  
        return f'<Card UID: {self.card_uid}, Student ID: {self.student_id}, Status: {self.status.value}>'