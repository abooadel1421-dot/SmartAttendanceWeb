# app/auth/__init__.py  
from flask import Blueprint  

bp = Blueprint('auth_bp', __name__)  

# استيراد المسارات بعد تعريف الـ Blueprint لتجنب مشاكل الاستيراد الدائرية  
from app.auth import routes