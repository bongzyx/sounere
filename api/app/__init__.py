from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'testing'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # migrate.init_app(app, db)
    return app


app = create_app()
db = SQLAlchemy(app)


def register_routes():
    from app.routes.api import api
    app.register_blueprint(api)


register_routes()
