# app/reports/__init__.py  
from flask import Blueprint  

bp = Blueprint('reports', __name__) # هنا يتم تعريف bp مرة واحدة فقط  

# استيراد الـ routes هنا بعد تعريف bp  
from app.reports import routes