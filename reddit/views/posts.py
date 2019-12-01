from flask import Blueprint, render_template
from flask_login import login_required

from reddit.models import Post

posts = Blueprint('posts', __name__)


@posts.route('', methods=['GET'])
@login_required
def posts_root():
    posts_from_db = Post.query.all()
    return render_template('posts.html', posts=posts_from_db)
