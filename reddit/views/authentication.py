from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session
from flask_login import login_user, current_user, login_required, logout_user

from reddit.database import db
from reddit.forms import LoginForm, RegisterForm
from reddit.models import User

authentication = Blueprint('authentication', __name__)


@authentication.route('/login', methods=['GET', 'POST'])
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
                    login_user(user, remember=True)
                    if current_user.is_authenticated:
                        session['username'] = user.name
                    next_url = request.args.get('next')
                    return redirect(next_url or url_for('root.home'))

        flash('Invalid username or password')
        return redirect('login')
    return render_template('login.html', form=form)


@authentication.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')

            if User.query.filter_by(email=email).first() is not None:
                flash('The email is already taken')
                return redirect('register')
            user = User(name, email, password)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            if current_user.is_authenticated:
                session['username'] = user.name
            next_url = request.args.get('next')
            return redirect(next_url or url_for('root.home'))

        flash('Invalid registration data')
        return redirect('register')
    return render_template('register.html', form=form)


@authentication.route("/logout")
def logout():
    logout_user()
    session['username'] = None

    return redirect(url_for('root.home'))
