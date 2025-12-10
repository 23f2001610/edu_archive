import os
import secrets
import string
from app import app, db
from models import Admin

def generate_secure_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_admin():
    with app.app_context():
        existing_admin = Admin.query.filter_by(username='admin').first()
        if not existing_admin:
            admin_password = os.environ.get('ADMIN_PASSWORD')
            
            if not admin_password:
                admin_password = generate_secure_password()
                print("=" * 50)
                print("ADMIN ACCOUNT CREATED")
                print("=" * 50)
                print(f"Username: admin")
                print(f"Password: {admin_password}")
                print("=" * 50)
                print("IMPORTANT: Save this password securely!")
                print("Set ADMIN_PASSWORD environment variable to use a custom password.")
                print("=" * 50)
            else:
                print("Admin user created with password from environment variable.")
            
            admin = Admin(username='admin')
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
        else:
            print("Admin user already exists")

if __name__ == '__main__':
    create_admin()

