from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os

db = SQLAlchemy()
#Name of Database
DB_NAME = "waterdb"


def create_app():
    #Initializes App
    app = Flask(__name__)

    #Registers All Blueprints
    from .auth import auth
    from .views import views
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix="/")

    #App Configs
    app.config["SECRET_KEY"] = "hello"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    #Max Length of Cookie Session
    app.permanent_session_lifetime = timedelta(minutes=20)

    #Creates Database if it hasnt been already
    from .models import users, cities, streets, addresses
    create_database(app)

    return app

def create_database(app):
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app=app)
