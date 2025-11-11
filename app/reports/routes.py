# app/reports/routes.py  
from flask import render_template  
from flask_login import login_required  
from app.utils.permissions import permission_required, Role  
from app.reports import bp # <--- هذا السطر صحيح ويجب أن يبقى، لأنه يستورد bp من __init__.py  

@bp.route('/')  
@bp.route('/index')  
# @login_required # علّق هذا السطر مؤقتًا إذا كنت تريد الوصول للصفحة بدون تسجيل دخول  
# @permission_required(Role.ADMIN) # علّق هذا السطر مؤقتًا لتجاوز مشكلة الصلاحيات  
def index():  
    return render_template('reports/index.html', title='التقارير')