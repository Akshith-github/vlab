from flask import Flask,url_for,session
# from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

# bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = '/auth/login'

def flash2(msg):
    if(session.get("msgs") is None):
        session['msgs']=[]
    session['msgs']=session['msgs'].append(msg)

def get_flashed2_messages():
    if(session.get("msgs")):
        for msg in session.get("msgs"):
            session['msgs'].remove(msg)
            yield msg

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .course import course as course_blueprint
    app.register_blueprint(course_blueprint,url_prefix='/course')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.jinja_env.globals.update(flash2=flash2)
    app.jinja_env.globals.update(get_flashed2_messages=get_flashed2_messages)
    return app



