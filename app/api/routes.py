from flask import request, jsonify, current_app, Blueprint
from app.models.student import Student
from app.models.card import Card
from app.models.attendance_log import AttendanceLog, AttendanceStatus
from app.models.device import Device
from datetime import datetime
from app import db # تأكد أن هذا يستورد 'db' و 'r' إن أمكن
import time
# import redis # لم نعد نحتاج لاستيراد redis هنا مباشرة إذا استوردنا 'r' من app
import uuid
from app.services.websocket_handler import socketio

# ==============================================================================
# الخطوة 1: استورد كائن Redis 'r' المعرف والمهيأ في app/__init__.py
# هذا يضمن أن 'r' يستخدم متغير البيئة REDIS_URL على Render.
from app import r
# ==============================================================================

api_bp = Blueprint('api', __name__)

# ==============================================================================
# لم نعد بحاجة لهذا السطر لأنه تم تهيئة 'r' في app/__init__.py
# r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
# ==============================================================================

SCAN_SESSION_PREFIX = "scan_session:"
SCAN_UID_PREFIX = "scan_uid:"

# ==============================================================================
# دالة مساعدة للتحقق من اتصال Redis
def check_redis_connection():
    if r is None:
        current_app.logger.error("Redis connection is not available.")
        return False
    try:
        r.ping()
        return True
    except Exception as e:
        current_app.logger.error(f"Redis connection failed: {e}")
        return False
# ==============================================================================

@api_bp.route('/admin/check-scanned-uid', methods=['GET'])
def check_scanned_uid():
    if not check_redis_connection():
        return jsonify({"success": False, "message": "Redis service unavailable"}), 500

    session_id = request.headers.get('X-Session-ID')
    if not session_id:
        return jsonify({"success": False, "message": "معرف الجلسة مفقود"}), 400

    uid = r.get(SCAN_UID_PREFIX + session_id)

    if uid:
        r.delete(SCAN_UID_PREFIX + session_id)
        return jsonify({
            "success": True,
            "card_uid": uid,
            "message": "تم مسح البطاقة بنجاح"
        }), 200
    else:
        return jsonify({
            "success": False,
            "message": "لا توجد بطاقة ممسوحة بعد"
        }), 404

@api_bp.route('/admin/scan-card-for-form', methods=['POST'])
def start_card_scan_for_form():
    if not check_redis_connection():
        return jsonify({"success": False, "message": "Redis service unavailable"}), 500

    current_app.logger.debug("--- DEBUG: Starting new scan session ---")

    session_id = request.headers.get('X-Session-ID')
    if not session_id:
        return jsonify({"success": False, "message": "معرف الجلسة مفقود"}), 400

    r.set(SCAN_SESSION_PREFIX + "active", session_id, ex=70)
    r.delete(SCAN_UID_PREFIX + session_id)

    current_app.logger.debug(f"--- DEBUG: Session {session_id} activated in Redis ---")

    return jsonify({
        "success": True,
        "message": "جلسة المسح نشطة",
        "session_id": session_id
    }), 200

@api_bp.route('/admin/cancel-card-scan', methods=['POST'])
def cancel_card_scan():
    if not check_redis_connection():
        return jsonify({"success": False, "message": "Redis service unavailable"}), 500

    session_id = request.headers.get('X-Session-ID')
    if not session_id:
        current_app.logger.error("X-Session-ID header is missing for cancel request.")
        return jsonify({"success": False, "message": "معرف الجلسة مفقود."}), 400

    active_session_id = r.get(SCAN_SESSION_PREFIX + "active")
    if active_session_id == session_id:
        r.delete(SCAN_SESSION_PREFIX + "active")
        r.delete(SCAN_UID_PREFIX + session_id)
        current_app.logger.info(f"Admin form scan cancelled by session: {session_id}")
        return jsonify({"success": True, "message": "تم إلغاء عملية المسح."}), 200
    else:
        current_app.logger.warning(f"Cancel request from {session_id} for non-matching scan {active_session_id}.")
        return jsonify({"success": False, "message": "لا توجد عملية مسح نشطة لهذه الجلسة."}), 404
@api_bp.route('/admin_scan_uid', methods=['POST'])
def receive_admin_scan_uid_from_esp():
    if not request.is_json:
        return jsonify({"message": "Request must be JSON"}), 400

    data = request.get_json()
    card_uid = data.get('card_uid')
    device_serial_number = data.get('device_serial_number')

    if not card_uid:
        return jsonify({"success": False, "message": "UID is required"}), 400
    if not device_serial_number:
        return jsonify({"message": "Missing 'device_serial_number' in request"}), 400

    current_app.logger.info(f"ESP32 received UID: {card_uid} from device: {device_serial_number}.")
    current_app.logger.debug(f"DEBUG: ESP32 sent UID: {card_uid}, Device: {device_serial_number}") # سجل جديد

    # ==============================================================================
    # الخطوة 2: أضف فحص اتصال Redis هنا
    if not check_redis_connection():
        current_app.logger.error("DEBUG: Redis connection failed in receive_admin_scan_uid_from_esp.") # سجل جديد
        return jsonify({"success": False, "message": "Redis service unavailable"}), 500
    # ==============================================================================

    active_session_id = r.get(SCAN_SESSION_PREFIX + "active")
    current_app.logger.debug(f"DEBUG: Retrieved active_session_id from Redis: {active_session_id}") # سجل جديد

    if active_session_id:
        # بما أن active_session_id هي بالفعل str، لا نحتاج لـ .decode()
        # فقط قم بتعيينها مباشرة أو استخدمها كما هي.
        decoded_active_session_id = active_session_id # <--- تم تعديل هذا السطر
        target_redis_key = SCAN_UID_PREFIX + decoded_active_session_id
        
        current_app.logger.debug(f"DEBUG: Entering admin scan block. Attempting to store UID: {card_uid} with key: {target_redis_key}")
        
        r.set(target_redis_key, card_uid, ex=10) 
        current_app.logger.info(f"UID {card_uid} stored for admin form session: {decoded_active_session_id}")
        return jsonify({"success": True, "message": "UID received and processed for admin form."}), 200
    else:
        current_app.logger.debug(f"DEBUG: No active admin form scan found. Entering attendance scan block.") # سجل جديد
        current_app.logger.info(f"No active admin form scan. Processing UID {card_uid} for attendance.")

        # 1. البحث عن الجهاز
        device = Device.query.filter_by(serial_number=device_serial_number).first()
        if not device:
            current_app.logger.warning(f"Unauthorized device with serial number: {device_serial_number}")
            return jsonify({"message": "Unauthorized Device", "status": "error"}), 403

        device.last_seen = datetime.utcnow()
        db.session.commit()

        # 2. البحث عن البطاقة
        card = Card.query.filter_by(card_uid=card_uid).first()

        if not card:
            current_app.logger.warning(f"No card found for UID: {card_uid}")
            return jsonify({"message": "Unauthorized Card UID", "status": "error"}), 401

        # 3. البحث عن الطالب
        student = card.student

        if not student:
            current_app.logger.error(f"Card UID {card_uid} found but no student linked.")
            return jsonify({"message": "Card not linked to any student", "status": "error"}), 404

        # 4. تسجيل الدخول/الخروج
        last_log = AttendanceLog.query.filter_by(student_id=student.id)\
                                      .order_by(AttendanceLog.timestamp.desc())\
                                      .first()

        new_status = AttendanceStatus.ENTER

        if last_log:
            if last_log.status == AttendanceStatus.ENTER:
                new_status = AttendanceStatus.EXIT

        new_log = AttendanceLog(
            student_id=student.id,
            card_id=card.id,
            device_id=device.id,
            status=new_status,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_log)
        db.session.commit()

        action_message = "entered" if new_status == AttendanceStatus.ENTER else "exited"
        current_app.logger.info(f"Student {student.full_name} (ID: {student.student_id_number}) {action_message} via device {device.name}.")

        # ✅ إرسال السجل الجديد عبر WebSocket فوراً
        try:
            socketio.emit('new_attendance_log', {
                'id': new_log.id,
                'student_name': student.full_name,
                'student_id_number': student.student_id_number,
                'device_name': device.name,
                'device_location': device.location,
                'status': new_status.value,  # 'ENTER' أو 'EXIT'
                'timestamp': new_log.timestamp.isoformat()
            }, namespace='/', skip_sid=None)
            current_app.logger.info(f"WebSocket event emitted for student {student.full_name}")
        except Exception as e:
            current_app.logger.error(f"Error emitting WebSocket event: {str(e)}")

        return jsonify({
            "message": f"Student {student.full_name} {action_message} successfully.",
            "status": new_status.value,
            "student_name": student.full_name,
            "action": action_message
        }), 200