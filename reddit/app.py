import os

from flask import Flask, request, abort, render_template

from reddit.models import User, Subreddit, Post, Comment
from reddit.security import login_manager, bcrypt
from reddit.views.authentication import authentication
from reddit.views.root import root
from reddit.views.subreddits import subreddits
from reddit.views.posts import posts
from reddit.views.chat import chat
from reddit.views.ws import ws

from .database import db
from .sockets import sockets


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # initalize modules
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    sockets.init_app(app)

    # register app blueprints
    app.register_blueprint(root)
    app.register_blueprint(authentication)
    app.register_blueprint(subreddits, url_prefix='/subreddits')
    app.register_blueprint(posts, url_prefix='/posts')
    app.register_blueprint(chat, url_prefix='/chat')

    # register ws blueprints
    sockets.register_blueprint(ws, url_prefix='/ws')

    return app


def add_default_user():
    user = User('admin@example.com', 'Admin', 'admin')

    db.session.add(user)
    db.session.commit()

    return user


def add_default_subreddit(user):
    subreddit = Subreddit(user_id=user.id, title='RZNU subreddit', description='Nothing special here')

    db.session.add(subreddit)
    db.session.commit()

    return subreddit


def add_default_subreddit_posts(user, subreddit):
    post1 = Post(user_id=user.id, title=f'First post by user {user.name}',
                 content=f'Some content here made by user {user.name}', subreddit_id=subreddit.id)
    post2 = Post(user_id=user.id, title=f'Second post by user {user.name}',
                 content=f'Some content here made by user {user.name}', subreddit_id=subreddit.id)

    db.session.add(post1)
    db.session.add(post2)
    db.session.commit()

    return [post1, post2]


def add_default_post_comments(user, posts):
    for post in posts:
        comment1 = Comment(content=f'I commented on my own post...', user_id=user.id, post_id=post.id)
        comment2 = Comment(content=f'Some comments here and there', user_id=user.id, post_id=post.id)
        db.session.add(comment1)
        db.session.add(comment2)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    if isinstance(user_id, int):
        return User.query.filter_by(id=user_id).first()
    return User.query.filter_by(email=user_id).first()


@login_manager.request_loader
def login_with_basic_auth(request):
    auth = request.authorization
    if not auth:
        return

    user = User.query.filter_by(email=auth.username).first()
    if not user or not user.check_password(auth.password):
        abort(401)

    return user


app = create_app()


@app.route('/documentation')
def get_docs():
    return render_template('documentation.html')


if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # to prevent flask issues with double initialization in debug mode
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = add_default_user()
        subreddit = add_default_subreddit(user)
        posts = add_default_subreddit_posts(user, subreddit)
        add_default_post_comments(user, posts)


if __name__ == "__main__":
    # run with embedded WSGIServer
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    print('Starting the app')
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
