from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_apscheduler import APScheduler
from os import path
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# app runs task after this many seconds to look for reminders and send texts
TEXT_INTERVAL = 15

db = SQLAlchemy()
db_name = "db.sqlite"

def create_app():
    app = Flask(__name__)

    # secret key used to sign cookies
    app.config['SECRET_KEY'] = b'asde{}=jk23432_"?2'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    # ----------- login/auth

    login_manager = LoginManager()
    # redirects to this page if non-logged-in user tries to access profile
    login_manager.login_view = 'auth.login' 
    login_manager.login_message = 'Please log in to view this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)
    
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # ---------- database

    db.init_app(app)
    # create a new database if one doesn't exist
    if not path.exists(db_name):
        db.create_all(app=app)

    # blueprint for user authentication routes of app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for dosage tracker parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # --------- apscheduler/time checking

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()

    from .textreminders import send_reminders

    def send_reminders_job():
        send_reminders(scheduler)

    scheduler.add_job(id='send reminders', func=send_reminders_job, trigger='interval', seconds=TEXT_INTERVAL)
    


    return app


