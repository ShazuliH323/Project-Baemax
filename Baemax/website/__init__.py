from flask import Flask

#databases and auth
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

#webchat stuff
from flask_socketio import join_room, leave_room , send, SocketIO 
import random
from string import ascii_uppercase

db = SQLAlchemy()
socketio = SocketIO()

def create_web():
    web = Flask(__name__)
    web.config['SECRET_KEY'] = 'ihatewendy'
    
    web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(web)
    "hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiij"
    

    from .models import User
    with web.app_context():
        db.create_all()


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(web)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #looking for primary key


    from .views import views
    from .auth import auth

    web.register_blueprint(views, url_prefix='/')
    web.register_blueprint(auth, url_prefix='/')


    socketio.init_app(web)
    
    

   
    web.static_folder = 'static'
    return web, socketio


