from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired('Please enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired('Enter your password!')])
    submit = SubmitField('Log in')


class RegisterForm(Form):
    name = StringField('Name', validators=[DataRequired('Enter your name')])
    email = StringField('Email', validators=[DataRequired('Enter an email')])
    password = PasswordField('Password', validators=[DataRequired('Enter your desired password')])

    submit = SubmitField('Register')


class SubredditForm(Form):
    title = StringField('Title', validators=[DataRequired('Please enter subreddit title')])
    description = StringField('Description', validators=[DataRequired('Please enter subreddit description')], widget=TextArea())
    submit = SubmitField('Create new subreddit')


class PostForm(Form):
    title = StringField('Title', validators=[DataRequired('Please enter post title')])
    content = StringField('Content', validators=[DataRequired('Please enter post content')], widget=TextArea())
    submit = SubmitField('Create new post')
