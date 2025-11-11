# app/attendance/__init__.py  
from flask import Blueprint  

bp = Blueprint('attendance', __name__, url_prefix='/attendance')  

# استيراد الـ routes هنا بعد تعريف bp  
from app.attendance import routes