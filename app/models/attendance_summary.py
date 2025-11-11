# app/models/attendance_summary.py

from app import db 
from datetime import date, time

class AttendanceSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False) 
    end_time = db.Column(db.Time, nullable=False)   
    location = db.Column(db.String(120), nullable=False) 
    status = db.Column(db.String(50), nullable=False) 
    actual_entry_time = db.Column(db.Time, nullable=True) 
    
    # العلاقة من جانب AttendanceSummary نحو Student
    # 'attendance_summaries' هو اسم العلاقة في نموذج Student
    student = db.relationship('Student', back_populates='attendance_summaries')

    __table_args__ = (db.UniqueConstraint('student_id', 'report_date', 'start_time', 'location', name='_student_attendance_summary_uc'),)

    def __repr__(self):
        return f'<AttendanceSummary StudentID:{self.student_id} - Date:{self.report_date} - Status:{self.status}>'
