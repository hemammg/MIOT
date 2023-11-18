from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)], 
                           render_kw={"placeholder": "Enter your username"})
    email = StringField('Email', 
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "example@example.com"})
    password = PasswordField('Password', 
                             validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your password"})
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')],
                                     render_kw={"placeholder": "Confirm your password"})
    submit = SubmitField('Sign Up')

    # Extra validation to check if the username or email is already taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "example@example.com"})
    password = PasswordField('Password', 
                             validators=[DataRequired()],
                             render_kw={"placeholder": "Enter your password"})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                           validators=[DataRequired(), Length(min=2, max=20)],
                           render_kw={"placeholder": "Enter your new username"})
    email = StringField('Email', 
                        validators=[DataRequired(), Email()],
                        render_kw={"placeholder": "example@example.com"})
    submit = SubmitField('Update')

    # Extra validation to avoid conflict with existing usernames/emails
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is already registered.')
