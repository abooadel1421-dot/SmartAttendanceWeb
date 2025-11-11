# app/models/student.py

from app import db
from datetime import datetime, date
import pytz
# 🟢 استورد نموذج AttendanceSummary هنا مباشرة
from .attendance_summary import AttendanceSummary # هذا هو التعديل الأساسي

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=True, index=True) # <--- هنا التغيير
    
    student_id_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)

    parent_email = db.Column(db.String(120), nullable=True, index=True)
    parent_phone_number = db.Column(db.String(20), nullable=True)

    grade = db.Column(db.String(10), nullable=True)
    major = db.Column(db.String(64), nullable=True)

    date_of_birth = db.Column(db.Date, nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc), onupdate=lambda: datetime.now(pytz.utc))
    is_active = db.Column(db.Boolean, default=True)
    enrollment_date = db.Column(db.DateTime, default=datetime.utcnow)

    # علاقات (Relationships) مع نماذج أخرى
    card = db.relationship('Card', back_populates='student', uselist=False)
    attendance_records = db.relationship('AttendanceLog', back_populates='student', lazy='dynamic')
    user_account = db.relationship('User', back_populates='student_profile', uselist=False)
    
    # العلاقة الجديدة مع AttendanceSummary
    # الآن 'AttendanceSummary' يمكن رؤيتها لأننا قمنا باستيرادها
    attendance_summaries = db.relationship('AttendanceSummary', back_populates='student', lazy='dynamic')


    def __repr__(self):
        return f'<Student {self.full_name} ({self.student_id_number})>'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return None
