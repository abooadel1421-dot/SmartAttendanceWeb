from flask import Blueprint

bp = Blueprint(
    'student',
    __name__,
    template_folder='templates',  # ✅ للـ templates
    url_prefix='/student'          # ✅ للـ URLs - مهم جداً!
)

# استيراد الـ routes بعد تعريف الـ Blueprint
from app.student import routes