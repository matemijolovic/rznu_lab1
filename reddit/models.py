from . import db


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), index=True, nullable=False, unique=True)
    name = db.Column(db.String(128), index=True, nullable=False)
