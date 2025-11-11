from datetime import datetime
from app import db
import pytz

SAUDIA_TZ = pytz.timezone('Asia/Riyadh')

class Notification(db.Model):
    __tablename__ = 'notification'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime, 
        default=lambda: datetime.now(SAUDIA_TZ).astimezone(pytz.utc),
        nullable=False
    )
    status = db.Column(db.String(20), default='unread', nullable=False)  # ✅ String بدل Enum
    type = db.Column(db.String(255), default='general', nullable=False)   # ✅ String بدل Enum
    link = db.Column(db.String(255), nullable=True)

    # العلاقات:
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_notifications', lazy=True)
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_notifications', lazy=True)

    def __repr__(self):
        return f"<Notification {self.id} from {self.sender_id} to {self.receiver_id}>"