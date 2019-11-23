import os

from flask import render_template, Flask

from reddit.models import User, Subreddit, Post, Comment
from reddit.security import login_manager, bcrypt
from reddit.views.authentication import authentication
from reddit.views.root import root
from reddit.views.subreddits import subreddits
from .database import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # initalize modules
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    app.register_blueprint(root)
    app.register_blueprint(authentication)
    app.register_blueprint(subreddits, url_prefix='/subreddits')

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
    return User.query.filter_by(email=user_id).first()


app = create_app()

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    # to prevent flask issues with double initialization in debug mode
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = add_default_user()
        subreddit = add_default_subreddit(user)
        posts = add_default_subreddit_posts(user, subreddit)
        add_default_post_comments(user, posts)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
