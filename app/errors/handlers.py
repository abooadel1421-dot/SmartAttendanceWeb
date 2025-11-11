# app/errors/handlers.py  
from flask import render_template  
from app.errors import bp  
from .. import db # نحتاج لاستيراد db للتعامل مع rollback في حالة خطأ 500  

@bp.app_errorhandler(404)  
def not_found_error(error):  
    return render_template('errors/404.html'), 404  

@bp.app_errorhandler(500)  
def internal_error(error):  
    db.session.rollback() # التراجع عن أي تغييرات معلقة في قاعدة البيانات في حالة حدوث خطأ 500  
    return render_template('errors/500.html'), 500