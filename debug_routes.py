from app import create_app

app, socketio = create_app()

print("\n" + "="*60)
print("🔍 ALL REGISTERED ROUTES:")
print("="*60)

with app.app_context():
    for rule in app.url_map.iter_rules():
        print(f"{rule.rule:50} -> {rule.endpoint}")

print("\n" + "="*60)
print("🔍 STUDENT ROUTES ONLY:")
print("="*60)

with app.app_context():
    for rule in app.url_map.iter_rules():
        if 'student' in str(rule):
            print(f"{rule.rule:50} -> {rule.endpoint}")

print("="*60 + "\n")