from werkzeug.security import generate_password_hash, check_password_hash
# import jwt

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    given_name = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(102))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def generate_auth_token(self, expires_in=600):
    #     return jwt.encode(
    #         {'id': self.id, 'exp': time.time() + expires_in},
    #         app.config['SECRET_KEY'], algorithm='HS256')

    # @staticmethod
    # def verify_auth_token(token):
    #     try:
    #         data = jwt.decode(token, app.config['SECRET_KEY'],
    #                           algorithm=['HS256'])
    #     except:
    #         return
    #     return User.query.get(data['id'])

    def __repr__(self):
        return f"User('{self.username}')"
