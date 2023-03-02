from flask import Flask, Blueprint
import os
import platform
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

db = SQLAlchemy()
load_dotenv()
SECRET_KEY = os.environ.get("SECRET_KEY")
DB_NAME = os.environ.get("DB_NAME")


def create_database(app):
    if not os.path.exists('/todolist/'+DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created DB!')

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"

    db.init_app(app)
    
    from .models import Note, User
    
    create_database(app)
    
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import user
    app.register_blueprint(user.user)
    
    from . import views
    app.register_blueprint(views.views)

    
    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=1)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app
