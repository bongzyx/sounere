from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
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
CORS(app)


def register_routes():
    from app.routes.auth import auth
    from app.routes.tools import tools
    from app.routes.requests import requests
    from app.routes.metadata import metadata
    from app.routes.search import search
    from app.routes.playlist import playlist

    app.register_blueprint(auth)
    app.register_blueprint(tools)
    app.register_blueprint(requests)
    app.register_blueprint(metadata)
    app.register_blueprint(search)
    app.register_blueprint(playlist)


register_routes()
