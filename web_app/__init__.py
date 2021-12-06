from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate


db = SQLAlchemy()
app = Flask(__name__)
migrate = Migrate(app, db)


# Do NOT share this
API_KEY = "3262a49e04d74260ab069b121615d08a"

basedir = os.path.abspath(os.path.dirname(__file__))


def init_app():
    app.config['SECRET_KEY'] = "CSE442"
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://vfgsppyukkdoud:c386c153945b1a2ccf02b07bdf28153250368968f120fe672a6c198977e52719@ec2-52-86-25-51.compute-1.amazonaws.com:5432/d8df4cdnbgr0ou"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .food import food

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(food, url_prefix="/")

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    from flask_apscheduler import APScheduler
    from .api_scheduler import store_recipes,send_email
    scheduler = APScheduler()
    scheduler.init_app(app)
    """Uncomment if you want to run the scheduler!
      So far its annoying to have everybody get emails to we comment this out """
    app.apscheduler.add_job(func=lambda: send_email(app), trigger = 'interval', seconds = 87535, id = 'EM1')
    #send_email(app)
    #app.apscheduler.add_job(func=lambda: store_recipes(app), trigger='interval', seconds=10, id="DB1")
    scheduler.start()

    return app


def create_database(app):
    if not os.path.exists("website/" + 'db.sqlite'):
        db.create_all(app=app)
        print("Created database!")
