from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from reddit.database import db
from reddit.security import bcrypt


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), index=True, nullable=False, unique=True)
    name = db.Column(db.String(128), index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    subreddits = relationship('Subreddit')
    posts = relationship('Post')
    comments = relationship('Comment')

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.set_password(password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Methods required by the flask-login
    def get_id(self):
        return self.email


class Subreddit(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    user = db.relationship('User', foreign_keys=user_id)
    title = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.String(256))
    posts = relationship('Post')


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    title = db.Column(db.String(128), nullable=False, unique=True)
    content = db.Column(db.String(2048))
    subreddit_id = db.Column(db.Integer, ForeignKey('subreddit.id'))


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(2048))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    post_id = db.Column(db.Integer, ForeignKey('post.id'))
