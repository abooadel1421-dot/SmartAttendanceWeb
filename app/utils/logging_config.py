# app/utils/logging_config.py  

import logging  
from logging.handlers import RotatingFileHandler  
import os  

def configure_logging(app):  
    """  
    يقوم بتهيئة نظام تسجيل الأحداث (logging) لتطبيق Flask.  
    """  
    # تعطيل تسجيل الأحداث الافتراضي لـ Werkzeug  
    # if not app.debug and not app.testing:  
    #     logging.getLogger('werkzeug').disabled = True  

    # تحديد مستوى التسجيل  
    app.logger.setLevel(logging.INFO)  

    # إنشاء مجلد للسجلات إذا لم يكن موجودًا  
    if not os.path.exists('logs'):  
        os.mkdir('logs')  

    # إعداد معالج الملفات الدوار (RotatingFileHandler)  
    # سيقوم بإنشاء ملف logs/app.log بحجم أقصى 10 كيلوبايت، ويحتفظ بـ 5 ملفات احتياطية.  
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=5, encoding='utf-8')  
    file_handler.setFormatter(logging.Formatter(  
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'  
    ))  
    file_handler.setLevel(logging.INFO)  
    app.logger.addHandler(file_handler)  

    # إعداد معالج الكونسول (إذا كنت ترغب في عرض السجلات في الكونسول أيضًا)  
    console_handler = logging.StreamHandler()  
    console_handler.setFormatter(logging.Formatter(  
        '%(asctime)s %(levelname)s: %(message)s'  
    ))  
    console_handler.setLevel(logging.INFO)  
    app.logger.addHandler(console_handler)  

    app.logger.info('تطبيق NFC Attendance System بدأ التشغيل')