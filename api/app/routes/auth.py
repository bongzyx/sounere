from flask import Blueprint, request, jsonify, url_for, abort

from app import db
from ..models.User import User
from app import jwt

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

auth = Blueprint('auth', __name__, url_prefix='/auth')


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(username=identity).one_or_none()


@auth.post('/register')
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


@auth.post('/login')
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return (jsonify({"error": "username or password not specified"}), 400)

    user = User.query.filter_by(username=username).first()
    if user:
        if user.verify_password(password):
            access_token = create_access_token(identity=username, fresh=True)
            refresh_token = create_refresh_token(identity=username)
            return jsonify(access_token=access_token, refresh_token=refresh_token)
        else:
            return (jsonify({"error": "wrong username or password"}), 400)
    else:
        return (jsonify({"error": "wrong username or password"}), 400)


@auth.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


@auth.post('/user')
@jwt_required(optional=True)
def user():
    current_identity = get_jwt_identity()
    if current_identity:
        return (jsonify({"yay": current_user.username}), 200)
    else:
        return jsonify(logged_in_as="anonymous user")


@auth.get('/test')
def test():
    return jsonify(logged_in_as="anonymous user")
