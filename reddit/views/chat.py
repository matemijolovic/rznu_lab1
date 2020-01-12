from flask import Blueprint, render_template
from flask_login import login_required, current_user

chat = Blueprint('chat', __name__)


@chat.route('')
@login_required
def multi_participant_chat():
    return render_template('chat.html', name=current_user.name)
