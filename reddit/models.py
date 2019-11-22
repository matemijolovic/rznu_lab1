from flask_login import UserMixin

from . import db, bcrypt


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), index=True, nullable=False, unique=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Methods required by the flask-login
    def get_id(self):
        return self.email

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
