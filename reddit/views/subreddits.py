from flask import Blueprint, render_template, redirect, request, abort, flash, url_for
from flask_login import login_required, current_user

from reddit.database import db
from reddit.forms import SubredditForm, PostForm, CommentForm
from reddit.models import Subreddit, Post, Comment

subreddits = Blueprint('subreddits', __name__)


@subreddits.route('', methods=['GET', 'POST'])
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


@subreddits.route('/<subreddit_id>', methods=['GET', 'DELETE'])
@login_required
def subreddit(subreddit_id):
    subreddit = Subreddit.query.filter_by(id=subreddit_id).first()
    if subreddit is None:
        abort(404)

    if request.method == 'DELETE':
        check_permission(subreddit)
        Subreddit.query.filter_by(id=subreddit_id).delete()
        db.session.commit()
        return redirect(url_for('subreddits.subreddits_root'))
    form = PostForm(request.form)
    return render_template('single_subreddit.html', form=form, subreddit=subreddit)


@subreddits.route('/<subreddit_id>/posts', methods=['POST'])
@login_required
def subreddit_posts(subreddit_id):
    subreddit = Subreddit.query.filter_by(id=subreddit_id).first()
    if subreddit is None:
        abort(404)
    form = PostForm(request.form)

    if form.validate():
        post = Post(
            user_id=current_user.id,
            subreddit_id=subreddit.id,
            title=request.form.get('title'),
            content=request.form.get('content')
        )
        db.session.add(post)
        db.session.commit()
        return render_template('single_subreddit.html', form=form, subreddit=subreddit)
    flash('Invalid data entered')
    return render_template('single_subreddit.html', form=form, subreddit=subreddit)


@subreddits.route('/<subreddit_id>/posts/<post_id>', methods=['GET', 'DELETE'])
@login_required
def subreddit_post(subreddit_id, post_id):
    post = find_post(subreddit_id, post_id)
    if request.method == 'DELETE':
        check_permission(post)
        Post.query.filter_by(id=post.id).delete()
        db.session.commit()
        return redirect(url_for('subreddits.subreddit', subreddit_id=subreddit_id))

    form = CommentForm(request.form)
    return render_template('single_post.html', post=post, form=form)


@subreddits.route('/<subreddit_id>/posts/<post_id>/comments', methods=['POST'])
@login_required
def subreddit_post_comments(subreddit_id, post_id):
    post = find_post(subreddit_id, post_id)
    form = CommentForm(request.form)

    if form.validate():
        comment = Comment(
            content=request.form.get('content'),
            user_id=current_user.id,
            post_id=post.id
        )
        db.session.add(comment)
        db.session.commit()
    return redirect(url_for('subreddits.subreddit_post', subreddit_id=subreddit_id, post_id=post_id))


@subreddits.route('/<subreddit_id>/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
@login_required
def subreddit_post_delete_comment(subreddit_id, post_id, comment_id):
    post = find_post(subreddit_id, post_id)
    comment = find_comment(comment_id, post)

    check_permission(comment)

    Comment.query.filter_by(id=comment.id).delete()
    db.session.commit()
    return redirect(url_for('subreddits.subreddit_post', subreddit_id=subreddit_id, post_id=post_id))


def find_post(subreddit_id, post_id):
    subreddit = Subreddit.query.filter_by(id=subreddit_id).first()
    if subreddit is None:
        abort(404)
    try:
        return next(filter(lambda post: post.id == int(post_id), subreddit.posts))
    except StopIteration:
        abort(404)


def find_comment(comment_id, post):
    if post is None:
        abort(404)

    try:
        return next(filter(lambda comment: comment.id == int(comment_id), post.comments))
    except StopIteration:
        abort(404)


def check_permission(comment):
    if comment.user_id != current_user.id:
        abort(403)
