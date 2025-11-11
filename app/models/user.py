# app/models/user.py  

from datetime import datetime  
from .. import db  
from werkzeug.security import generate_password_hash, check_password_hash  
from flask_login import UserMixin  
from enum import Enum  
import pytz  

class UserRole(Enum):  
    ADMIN = 'admin'  
    TEACHER = 'teacher'  
    STUDENT = 'student'  

class User(UserMixin, db.Model):  
    id = db.Column(db.Integer, primary_key=True)  
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)  
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)  
    password_hash = db.Column(db.String(128))  
    role = db.Column(db.Enum(UserRole), default=UserRole.TEACHER, nullable=False)  
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))  
    last_seen = db.Column(db.DateTime, nullable=True)  
    managed_devices = db.relationship('Device', back_populates='manager', cascade='all, delete-orphan')

    # --------------------------------------------------------------------------------------
    # المفتاح الأجنبي student_id يجب حذفه من هنا لأن المفتاح الأجنبي سيكون في Student
    # student_id = db.Column(db.Integer, db.ForeignKey('student.id', name='fk_user_student_id'), unique=True, nullable=True)  
    # --------------------------------------------------------------------------------------

    # العلاقة من User إلى Student  
    # student_profile هو اسم العلاقة في User
    student_profile = db.relationship('Student', back_populates='user_account', uselist=False)  

    # ... بقية الكود بدون تغيير
    def set_password(self, password):  
        self.password_hash = generate_password_hash(password)  

    def check_password(self, password):  
        return check_password_hash(self.password_hash, password)  

    def is_admin(self):  
        return self.role == UserRole.ADMIN  

    def is_teacher(self):  
        return self.role == UserRole.TEACHER  

    def is_student(self):  
        return self.role == UserRole.STUDENT  

    def __repr__(self):  
        return f'<User {self.username} (Role: {self.role.value})>'