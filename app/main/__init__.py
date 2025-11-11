from flask import Blueprint  

bp = Blueprint('main', __name__)  

from app.main import routes # استيراد المسارات بعد تعريف الـ Blueprint