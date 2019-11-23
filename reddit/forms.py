from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired('Please enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired('Enter your password!')])
    submit = SubmitField('Log in')


class RegisterForm(Form):
    name = StringField('Name', validators=[DataRequired('Enter your name')])
    email = StringField('Email', validators=[DataRequired('Enter an email')])
    password = PasswordField('Password', validators=[DataRequired('Enter your desired password')])

    submit = SubmitField('Register')
