import eventlet
eventlet.monkey_patch()

from app import create_app

# استدعاء دالة create_app لإنشاء كائن التطبيق وكائن socketio
app, socketio = create_app()

# ✅ الحل الصحيح للعمل مع Gunicorn و eventlet
# بدلاً من socketio.wsgi_app، استخدم app مباشرة
# Flask-SocketIO سيتولى إدارة WebSocket تلقائياً
application = app

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)