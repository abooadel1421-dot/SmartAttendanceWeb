from flask import render_template  
from app.main import bp # استيراد الـ Blueprint المعرف في __init__.py  
from flask_login import login_required # أضف هذا الاستيراد  

@bp.route('/')  
@bp.route('/index')  
def index():  
    return render_template('index.html', title='الصفحة الرئيسية')


# @bp.route('/dashboard')  
# @login_required  
# def dashboard():  
#     return render_template('main/dashboard.html', title='لوحة التحكم') # تأكد من مسار الـ template  
