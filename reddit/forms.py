from wtforms import Form, StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired('Please enter a valid email')])
    password = StringField('Password', validators=[DataRequired('Enter your password!')])
    submit = SubmitField('Log in')
