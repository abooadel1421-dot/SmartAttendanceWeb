import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-key-that-no-one-would-guess'

    # هذا هو التعديل الرئيسي: استخدام DATABASE_URL مباشرة
    # توفير قيمة افتراضية للبيئة المحلية (للتطوير)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              f"mysql+mysqlconnector://{os.environ.get('MYSQL_USER_LOCAL', 'root')}:" \
                              f"{os.environ.get('MYSQL_PASSWORD_LOCAL', '')}@" \
                              f"{os.environ.get('MYSQL_HOST_LOCAL', 'localhost')}:" \
                              f"{os.environ.get('MYSQL_PORT_LOCAL', '3306')}/" \
                              f"{os.environ.get('MYSQL_DATABASE_LOCAL', 'smart_nfc_attendance')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # إعدادات إضافية يمكن إضافتها لاحقًا:  

    # إعدادات البريد الإلكتروني (إذا كنت تخطط لإرسال إشعارات عبر البريد)  
    MAIL_SERVER = os.environ.get('MAIL_SERVER')  
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)  
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None  
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')  
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')  
    ADMINS = ['your-admin-email@example.com'] # قائمة بمسؤولي النظام  

    # إعدادات تسجيل الدخول (Flask-Login)  
    REMEMBER_COOKIE_DURATION = 3600 * 24 * 7 # تذكر المستخدم لمدة أسبوع (بالثواني)  

    # إعدادات الصفحات لكل صفحة (Pagination)  
    POSTS_PER_PAGE = 20 # مثال لعدد العناصر في الصفحة الواحدة  

    # إعدادات لغة التطبيق (إذا كنت تخطط لدعم لغات متعددة)  
    LANGUAGES = ['en', 'ar']  

    # إعدادات خاصة بالـ NFC/RFID (يمكن أن تكون هنا أو في ملفات الخدمات)  
    # NFC_READER_API_KEY = os.environ.get('NFC_READER_API_KEY')  
    # NFC_READER_BASE_URL = os.environ.get('NFC_READER_BASE_URL')