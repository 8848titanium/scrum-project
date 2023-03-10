from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from wtforms_validators import Integer

from app_pkg.models import *


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(min=5, max=128)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=32)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate_email(self, email):
        self.email = self.email
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('This email not registered!')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None or not user.check_password(password.data):
            raise ValidationError('Invalid password!')


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired(), Length(max=32)])
    email = StringField('Email:', validators=[DataRequired(), Email(), Length(min=5, max=128)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=8, max=32)])
    password2 = PasswordField(
        'Confirm Password:', validators=[DataRequired(), EqualTo('password')])
    type = BooleanField()
    submit = SubmitField('Register and Login')

    def validate_username(self, username):
        self.username = self.username
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please user a different username.')

    def validate_email(self, email):
        self.email = self.email
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class JoinQuizForm(FlaskForm):
    pin = StringField(validators=[DataRequired(), Length(min=6, max=6), Integer()])
    submit = SubmitField('Join Now')

    def validate_pin(self, pin):
        self.pin = self.pin
        quiz = Quiz.query.filter_by(pin=pin.data).first()
        if quiz is None:
            raise ValidationError('Please try a different pin.')


class QuestionForm(FlaskForm):
    question = StringField('Question:', validators=[DataRequired()])
    choice_a = StringField('Choice A:', validators=[DataRequired()])
    checkbox_a = BooleanField()
    choice_b = StringField('Choice B:', validators=[DataRequired()])
    checkbox_b = BooleanField()
    choice_c = StringField('Choice C:', validators=[DataRequired()])
    checkbox_c = BooleanField()
    choice_d = StringField('Choice D:', validators=[DataRequired()])
    checkbox_d = BooleanField()
    submit = SubmitField('Submit question')


class QuizNameForm(FlaskForm):
    name = StringField('Quiz Name:', validators=[DataRequired()])
    submit = SubmitField('Apply Name Changes')
