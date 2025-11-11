from flask import Blueprint  

# تعريف الـ Blueprint أولاً  
teacher_bp = Blueprint(  
    'teacher',  
    __name__,  
    url_prefix='/teacher',  
    template_folder='templates'  
)  

# ثم، استيراد المسارات من نفس المجلد  
# هذا الاستيراد يجب أن يكون في نهاية الملف أو بعد تعريف الـ Blueprint مباشرةً  
# لضمان أن teacher_bp قد تم تعريفه قبل أن تحاول routes.py استخدامه.  
from . import routes