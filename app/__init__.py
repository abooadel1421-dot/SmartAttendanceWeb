# app/__init__.py

# ==============================================================================
# أضف استيراد eventlet هنا أولاً وقم بالـ monkey_patch
# هذا يضمن أن يتم تطبيق الـ monkey-patching قبل استيراد أي مكتبات أخرى قد تتأثر
import eventlet
eventlet.monkey_patch()
# ==============================================================================

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l

# ==============================================================================
# أضف استيراد Redis
import redis
# ==============================================================================

# ==============================================================================
# أضف استيراد Flask-SocketIO
from flask_socketio import SocketIO
# ==============================================================================


# db, migrate, login, bootstrap, moment, babel يتم تعريفهم هنا كمتغيرات على مستوى الوحدة
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel() # تهيئة Babel هنا (كائن Babel)

# ==============================================================================
# تعريف كائن Redis على مستوى الوحدة
# سيتم تهيئته لاحقًا في create_app
r = None
# ==============================================================================

# ==============================================================================
# تعريف كائن SocketIO على مستوى الوحدة
socketio = SocketIO()
# ==============================================================================


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'auth_bp.login'
    login.login_message = _l('الرجاء تسجيل الدخول للوصول إلى هذه الصفحة.')
    login.login_message_category = 'info'
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app) # تهيئة Babel مع التطبيق هنا

    # ----------------------------------------------------------------------
    # ** التصحيح لـ Babel.localeselector_func **
    # تعريف الدالة get_locale هنا
    def get_locale():
        return 'ar'

    # تعيين الدالة إلى babel.localeselector_func بعد تهيئة Babel بالتطبيق
    babel.localeselector_func = get_locale
    # ----------------------------------------------------------------------

    # ==============================================================================
    # تهيئة Redis هنا
    global r # استخدم الكائن r المعرف عالميًا

    redis_url = os.environ.get('REDIS_URL') or app.config.get('REDIS_URL') # تأكد من البحث في app.config أيضاً

    if redis_url:
        try:
            r = redis.from_url(redis_url, decode_responses=True)
            r.ping()
            app.logger.info("Connected to Redis using REDIS_URL environment variable successfully!")
        except redis.exceptions.ConnectionError as e:
            app.logger.error(f"Error connecting to Redis via REDIS_URL: {e}")
            r = None # Redis غير متاح
    else:
        app.logger.warning("REDIS_URL environment variable not found. Attempting connection to localhost for local development.")
        try:
            r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
            r.ping()
            app.logger.info("Connected to local Redis successfully!")
        except redis.exceptions.ConnectionError as e:
            app.logger.error(f"Error connecting to local Redis: {e}. Redis functionality will be disabled.")
            r = None # Redis غير متاح محلياً أيضاً
    # ==============================================================================

    # ==============================================================================
    # قم بتهيئة Flask-SocketIO هنا
    # استخدم Redis كوسيط للرسائل (message_queue)
    # تأكد من أن Redis_URL متاح!
    if redis_url: # تأكد أن redis_url تم تحديده
        socketio.init_app(app, message_queue=redis_url, cors_allowed_origins="*")
        app.logger.info(f"SocketIO initialized with Redis message queue: {redis_url}")
    else:
        # إذا لم يكن Redis متاحاً، فلا يمكن لـ SocketIO العمل بشكل صحيح مع Gunicorn workers
        # أو استخدم الوضع الافتراضي لـ SocketIO (لا يدعم multi-worker)
        socketio.init_app(app, cors_allowed_origins="*")
        app.logger.warning("Redis URL not found, SocketIO initialized without message queue. Multi-worker support will be limited.")
    # ==============================================================================


    from app.utils.logging_config import configure_logging
    configure_logging(app)

    # ------------------------------------------------------------------
    # استيراد النماذج
    from app.models.user import User, UserRole
    from app.models.student import Student
    from app.models.card import Card
    from app.models.attendance_log import AttendanceLog
    from app.models.device import Device
    # ------------------------------------------------------------------

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.context_processor
    def inject_enums():
        return dict(UserRole=UserRole)

    # *** ابدأ هنا باستيراد وتسجيل Blueprints داخل الدالة ***

    # ... (بقيت Blueprints كما هي، لم أقم بتضمينها هنا للاختصار) ...
    # Blueprint الخاص بالمصادقة (Auth Blueprint)
    try:
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        app.logger.debug(f"Blueprint 'auth_bp' registered successfully with URL prefix: {auth_bp.url_prefix}")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'auth_bp': {e}")


    # Blueprint الخاص بالإدارة (Admin Blueprint)
    try:
        from app.admin import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.logger.debug(f"Blueprint 'admin_bp' registered successfully with URL prefix: {admin_bp.url_prefix}")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'admin_bp': {e}")


    # Blueprint الخاص بالمعلم (Teacher Blueprint)
    try:
        from app.teacher import teacher_bp
        app.register_blueprint(teacher_bp, url_prefix='/teacher')
        app.logger.debug(f"Blueprint 'teacher_bp' registered successfully with URL prefix: {teacher_bp.url_prefix}")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'teacher_bp': {e}")

    # Blueprint الخاص بالطالب (Student Blueprint)
    try:
        from app.student import bp as student_bp

        app.register_blueprint(student_bp)
        app.logger.debug(f"Blueprint 'student_bp' registered successfully with URL prefix: {student_bp.url_prefix}")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'student_bp': {e}")

    # Blueprint الخاص بـ API
    try:
        # ==============================================================================
        # عند استيراد api_bp، ستحتاج إلى التأكد من أن api_bp لديه وصول إلى كائن Redis 'r'
        # إحدى الطرق هي تمريرها كوسيطة، أو ببساطة استيراد 'r' مباشرة من app/__init__.py
        # داخل routes.py
        # ==============================================================================
        from app.api.routes import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        app.logger.debug(f"Blueprint 'api_bp' registered successfully with URL prefix: {api_bp.url_prefix}")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'api_bp': {e}")

    # Blueprints الأخرى
    try:
        from app.errors import bp as errors_bp
        app.register_blueprint(errors_bp)
        app.logger.debug(f"Blueprint 'errors_bp' registered successfully.")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'errors_bp': {e}")

    try:
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)
        app.logger.debug(f"Blueprint 'main_bp' registered successfully.")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'main_bp': {e}")

    try:
        from app.students import bp as students_bp
        app.register_blueprint(students_bp, url_prefix='/students')
        app.logger.debug(f"Blueprint 'students_bp' registered successfully with URL prefix: {students_bp.url_prefix}")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'students_bp' with URL prefix: {students_bp.url_prefix}")

    try:
        from app.attendance import bp as attendance_bp
        app.register_blueprint(attendance_bp, url_prefix='/attendance')
        app.logger.debug(f"Blueprint 'attendance_bp' registered successfully with URL prefix: {attendance_bp.url_prefix}")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'attendance_bp': {e}")

    try:
        from app.reports import bp as reports_bp
        app.register_blueprint(reports_bp, url_prefix='/reports')
        app.logger.debug(f"Blueprint 'reports_bp' registered successfully with URL prefix: {reports_bp.url_prefix}")
    except Exception as e:
        app.logger.error(f"ERROR: Failed to register 'reports_bp': {e}")


    # إضافة مسار رئيسي أو صفحة هبوط
    @app.route('/')
    def index():
        return "مرحباً بكم في نظام الحضور والانصراف!"

    # ==============================================================================
    return app, socketio # ارجع كلاً من app و socketio
    # ==============================================================================