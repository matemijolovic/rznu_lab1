from flask import Blueprint, render_template, redirect, request, abort, flash, g
from flask_login import login_required, current_user

from reddit.database import db
from reddit.forms import SubredditForm, PostForm
from reddit.models import Subreddit, Post

subreddits = Blueprint('subreddits', __name__)


@subreddits.route('/', methods=['GET', 'POST'])
@login_required
def subreddits_root():
    subreddits = Subreddit.query.all()
    form = SubredditForm(request.form)
    if request.method == 'POST':
        if form.validate():
            subreddit = Subreddit(
                user_id=current_user.id,
                title=request.form.get('title'),
                description=request.form.get('description')
            )
            db.session.add(subreddit)
            db.session.commit()
            return redirect(f'/subreddits/{subreddit.id}')
        flash('Invalid data entered')
        return render_template('subreddits.html', form=form, subreddits=subreddits)
    return render_template('subreddits.html', form=form, subreddits=subreddits)


@subreddits.route('/<subreddit_id>', methods=['GET', 'POST'])
@login_required
def subreddit(subreddit_id):
    subreddit = Subreddit.query.filter_by(id=subreddit_id).first()
    if subreddit is None:
        abort(404)
    form = PostForm(request.form)

    if request.method == 'POST':
        if form.validate():
            post = Post(
                user_id=current_user.id,
                title=request.form.get('title'),
                content=request.form.get('content')
            )
            db.session.add(post)
            db.session.commit()
            return render_template('single_subreddit.html', form=form, subreddit=subreddit)
        flash('Invalid data entered')
        return render_template('single_subreddit.html', form=form, subreddit=subreddit)

    return render_template('single_subreddit.html', form=form, subreddit=subreddit)


@subreddits.route('/form', methods=['GET'])
@login_required
def new_subreddit_form():
    pass
