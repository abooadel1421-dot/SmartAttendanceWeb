# app/services/websocket_handler.py  

# هذه الوحدة ستعتمد بشكل كبير على Flask-SocketIO  
# تأكد من تثبيت Flask-SocketIO: pip install Flask-SocketIO  
from flask_socketio import SocketIO, emit  

# سيتم تهيئة SocketIO في __init__.py الخاص بالتطبيق الرئيسي  
socketio = SocketIO()  

class WebSocketService:  
    """  
    خدمة لإرسال تحديثات في الوقت الفعلي عبر WebSockets.  
    """  

    def emit_attendance_update(self, attendance_data: dict):  
        """  
        يرسل تحديثاً حول سجل حضور جديد أو متغير.  

        Args:  
            attendance_data (dict): قاموس يحتوي على تفاصيل سجل الحضور.  
                                    مثلاً: {'student_name': 'اسم الطالب', 'timestamp': 'الوقت', 'status': 'حاضر'}  
        """  
        emit('attendance_update', attendance_data, namespace='/', broadcast=True)  
        # 'namespace' يمكن أن يكون '/' أو '/dashboard' مثلاً  
        # 'broadcast=True' يعني إرسال لجميع العملاء المتصلين  

    def emit_daily_summary_update(self, summary_data: dict):  
        """  
        يرسل تحديثاً لملخص الحضور اليومي.  
        """  
        emit('daily_summary_update', summary_data, namespace='/', broadcast=True)  

    def handle_connect(self):  
        """يتم استدعاؤها عند اتصال عميل جديد."""  
        current_app.logger.info("عميل WebSocket متصل.")  
        # يمكن إرسال بيانات أولية للعميل الجديد هنا  

    def handle_disconnect(self):  
        """يتم استدعاؤها عند قطع اتصال عميل."""  
        current_app.logger.info("عميل WebSocket قطع الاتصال.")  

    # يمكن إضافة المزيد من معالجات الأحداث هنا  
    # مثل: @socketio.on('some_event')  

# في app/__init__.py، ستحتاج إلى:  
# from app.services.websocket_handler import socketio  
# # ...  
# def create_app(...):  
#     # ...  
#     socketio.init_app(app)  
#     # ...  
#     return app  

# وفي wsgi.py (أو حيث تشغل التطبيق مع SocketIO):  
# from app import create_app  
# from app.services.websocket_handler import socketio  
# app = create_app()  
# if __name__ == '__main__':  
#     socketio.run(app, debug=True)