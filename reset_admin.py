import os
import secrets
import string
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from app import app, db
from models import Admin

def generate_secure_password(length=16):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def reset_admin():
    with app.app_context():
        admin = Admin.query.filter_by(username='admin').first()
        
        if admin:
            # Get password from environment or generate new one
            admin_password = os.environ.get('ADMIN_PASSWORD')
            
            if not admin_password:
                admin_password = generate_secure_password()
            
            # Update the password
            admin.set_password(admin_password)
            db.session.commit()
            
            print("=" * 50)
            print("ADMIN PASSWORD RESET")
            print("=" * 50)
            print(f"Username: admin")
            print(f"Password: {admin_password}")
            print("=" * 50)
            print("IMPORTANT: Save this password securely!")
            print("=" * 50)
        else:
            print("Admin user does not exist. Run init_admin.py first.")

if __name__ == '__main__':
    reset_admin()

