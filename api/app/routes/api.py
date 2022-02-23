from flask import Blueprint, request, jsonify, url_for, abort
# from werkzeug.security import generate_password_hash, check_password_has

from app import db
from ..models.user import User

api = Blueprint('api', __name__, url_prefix='/api')


@api.post('/register')
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    given_name = request.json.get('given_name')

    if username is None or password is None:
        return (jsonify({"error": "username or password not specified"}), 400)

    if User.query.filter_by(username=username).first():
        return (jsonify({"error": "user already exists"}), 400)

    user = User(username=username, given_name=given_name)
    user.hash_password(password)

    db.session.add(user)
    db.session.commit()

    return (jsonify({"username": user.username, "given_name": user.given_name}), 201)
