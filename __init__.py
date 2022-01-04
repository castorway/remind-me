from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
db_name = "db.sqlite"

def create_app():
    app = Flask(__name__)

    # secret key used to sign cookies
    app.config['SECRET_KEY'] = b'asde{}=jk23432_"?2'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    login_manager = LoginManager()
    # redirects to this page if non-logged-in user tries to access profile
    login_manager.login_view = 'auth.login' 
    login_manager.login_message = 'Please log in to view this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)
    
    from .models import User

    # what is this for
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

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

    return app