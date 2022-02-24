from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testing'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # migrate.init_app(app, db)
    return app


app = create_app()
db = SQLAlchemy(app)
jwt = JWTManager(app)


def register_routes():
    from app.routes.auth import auth
    app.register_blueprint(auth)


register_routes()
