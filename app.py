from dotenv import load_dotenv
load_dotenv()


import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///edu_archive.db"

print(f"DEBUG: SQLALCHEMY_ENGINE_OPTIONS is: {app.config.get('SQLALCHEMY_ENGINE_OPTIONS')}")

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {}
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"



UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

with app.app_context():
    import models
    db.create_all()
