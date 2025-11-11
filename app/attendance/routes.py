# app/attendance/routes.py  
from flask import render_template  
from flask_login import login_required  
from app.utils.permissions import permission_required, Role  
from app.attendance import bp # هذا السطر صحيح ويجب أن يبقى  

@bp.route('/')  
@bp.route('/logs')  
@login_required  
# @permission_required(Role.ADMIN)  
def logs():  
    return render_template('attendance/logs.html', title='سجلات الحضور')