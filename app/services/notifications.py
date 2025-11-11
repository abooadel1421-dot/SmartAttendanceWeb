# app/services/notifications.py  

import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  
from flask import current_app # لاستخدام إعدادات التطبيق مثل البريد الإلكتروني وكلمة المرور  
from app.models.student import Student  
from app.models.user import User # لإرسال إشعارات للمستخدمين (مثلاً المعلمين/الإدارة)  

class NotificationService:  
    """  
    خدمة لإرسال الإشعارات عبر البريد الإلكتروني.  
    """  

    def __init__(self):  
        # يمكن قراءة الإعدادات من current_app.config  
        self.smtp_server = current_app.config.get('MAIL_SERVER')  
        self.smtp_port = current_app.config.get('MAIL_PORT')  
        self.smtp_username = current_app.config.get('MAIL_USERNAME')  
        self.smtp_password = current_app.config.get('MAIL_PASSWORD')  
        self.sender_email = current_app.config.get('MAIL_SENDER')  
        self.use_tls = current_app.config.get('MAIL_USE_TLS', True)  

    def _send_email(self, recipient_email: str, subject: str, body: str, is_html: bool = False):  
        """دالة داخلية لإرسال البريد الإلكتروني."""  
        if not all([self.smtp_server, self.smtp_port, self.smtp_username, self.smtp_password, self.sender_email]):  
            current_app.logger.error("إعدادات البريد الإلكتروني غير مكتملة. لا يمكن إرسال البريد.")  
            return False  

        msg = MIMEMultipart("alternative")  
        msg["From"] = self.sender_email  
        msg["To"] = recipient_email  
        msg["Subject"] = subject  

        if is_html:  
            msg.attach(MIMEText(body, "html", "utf-8"))  
        else:  
            msg.attach(MIMEText(body, "plain", "utf-8"))  

        try:  
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:  
                if self.use_tls:  
                    server.starttls()  
                server.login(self.smtp_username, self.smtp_password)  
                server.sendmail(self.sender_email, recipient_email, msg.as_string())  
            current_app.logger.info(f"تم إرسال بريد إلكتروني إلى {recipient_email} بعنوان: {subject}")  
            return True  
        except Exception as e:  
            current_app.logger.error(f"فشل في إرسال البريد الإلكتروني إلى {recipient_email}: {e}")  
            return False  

    def send_absence_notification(self, student: Student, teacher_email: str = None, parent_email: str = None) -> bool:  
        """  
        يرسل إشعاراً بالغياب لطالب معين.  
        """  
        subject = f"إشعار غياب: {student.full_name}"  
        body = f"""  
        <html>  
        <body dir="rtl" style="text-align: right; font-family: Arial, sans-serif;">  
            <p>السيد/السيدة المحترم/ة,</p>  
            <p>نود إعلامكم بأن الطالبة/الطالب <strong>{student.full_name}</strong> (رقم هوية: {student.id_number})   
            لم تسجل حضورها/حضوره في نظام الحضور الذكي اليوم.</p>  
            <p>الرجاء اتخاذ الإجراءات اللازمة أو التواصل مع الإدارة للمزيد من التفاصيل.</p>  
            <p>شكرًا,</p>  
            <p>إدارة نظام الحضور الذكي NFC</p>  
        </body>  
        </html>  
        """  
        
        sent_to_teacher = False  
        sent_to_parent = False  

        if teacher_email:  
            sent_to_teacher = self._send_email(teacher_email, subject, body, is_html=True)  
        
        # إذا كان للطالب بريد إلكتروني للولي  
        # if student.parent_email:   
        #     sent_to_parent = self._send_email(student.parent_email, subject, body, is_html=True)  
        
        return sent_to_teacher or sent_to_parent  

    def send_general_notification(self, recipient_email: str, subject: str, message: str) -> bool:  
        """  
        يرسل إشعاراً عاماً عبر البريد الإلكتروني.  
        """  
        return self._send_email(recipient_email, subject, message)  

# يجب أن تكون إعدادات البريد الإلكتروني في config.py  
# مثلاً:  
# MAIL_SERVER = 'smtp.googlemail.com'  
# MAIL_PORT = 587  
# MAIL_USE_TLS = True  
# MAIL_USERNAME = os.environ.get('EMAIL_USER')  
# MAIL_PASSWORD = os.environ.get('EMAIL_PASS')  
# MAIL_SENDER = 'your_email@example.com'