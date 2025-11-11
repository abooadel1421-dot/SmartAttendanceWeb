# app/admin/__init__.py  
from flask import Blueprint  
import os  

# احصل على المسار المطلق لمجلد admin  
basedir = os.path.abspath(os.path.dirname(__file__))  

# استخدم المسار المطلق الكامل  
admin_bp = Blueprint(  
    'admin',  
    __name__,  
    template_folder=os.path.join(basedir, 'templates'),  
    static_folder='static',  
    url_prefix='/admin'  
)  

# استيراد طرق العرض لتسجيلها مع الـ Blueprint  
from app.admin import routes