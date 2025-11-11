# app/models/excuse.py

from app import db
from datetime import datetime
import enum
import pytz

class ExcuseStatus(enum.Enum):
    PENDING = "pending"          # ✅ صح
    APPROVED = "approved"        # ✅ صح
    REJECTED = "rejected"        # ✅ صح

class Excuse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date_of_absence = db.Column(db.Date, nullable=False)
    reason = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))
    status = db.Column(db.Enum(ExcuseStatus), nullable=False, default=ExcuseStatus.PENDING)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    review_notes = db.Column(db.Text, nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    # علاقات
    student = db.relationship('Student', backref=db.backref('excuses', lazy='dynamic'))
    reviewer = db.relationship('User', foreign_keys=[reviewer_id], backref=db.backref('reviewed_excuses', lazy='dynamic'))

    def __repr__(self):
        return f'<Excuse {self.id} for {self.student.full_name} on {self.date_of_absence} - {self.status.value}>'