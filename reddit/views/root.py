from flask import Blueprint, render_template

from reddit.models import Subreddit

root = Blueprint('root', __name__)


@root.route('/')
def home():
    subreddits = Subreddit.query.all()[:5]
    return render_template('index.html', subreddits=subreddits)
