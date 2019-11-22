import flask
from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user

from reddit.forms import LoginForm
from reddit.models import User
from . import app, login_manager


@app.route('/')
def home():
    return render_template('index.html')


# TODO move to separate authentication blueprint
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate():
            # Get Form Fields
            email = request.form.get('email')
            password = request.form.get('password')
            # Validate Login Attempt
            user = User.query.filter_by(email=email).first()
            if user:
                if user.check_password(password=password):
                    login_user(user)
                    next = request.args.get('next')
                    return redirect(next or url_for('.home'))

        flash('Invalid username or password')
        return redirect('login')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(email=user_id)


if __name__ == '__main__':
    app.run()
