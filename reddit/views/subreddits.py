from flask import Blueprint, render_template, redirect, request, abort
from flask_login import login_required

from reddit.models import Subreddit

subreddits = Blueprint('subreddits', __name__)


@subreddits.route('/', methods=['GET', 'POST'])
@login_required
def subreddits_root():
    if request.method == 'POST':
        # TODO save new subreddit
        pass
    subreddits = Subreddit.query.all()
    return render_template('subreddits.html', subreddits=subreddits)


@subreddits.route('/<subreddit_id>', methods=['GET'])
@login_required
def subreddit(subreddit_id):
    subreddit = Subreddit.query.filter_by(id=subreddit_id).first()
    if subreddit is None:
        abort(404)
    return render_template('single_subreddit.html', subreddit=subreddit)


@subreddits.route('/form', methods=['GET'])
@login_required
def new_subreddit_form():
    pass
