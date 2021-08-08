from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
import re


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'Usernames must have only letters, numbers, dots or '
                'underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            flash('Email already registered')
            raise ValidationError('Email already registered.')
        if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@klu\.ac\.in$", field.data):
            flash('Not valid klu mail id')
            raise ValidationError('Mail id provided did not match pattern.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            flash('Username already in use.')
            raise ValidationError('Username already in use.')
    
    def validate_password2(self, field):
        if field.data!=self.data["password"]:
            flash('passwords are not same')
            raise ValidationError('Passwords are not same.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm new password',validators=[DataRequired()])
    submit = SubmitField('Update Password')

    def validate_password2(self, field):
        if field.data!=self.data["password"]:
            flash('passwords are not same')
            raise ValidationError('Passwords are not same.')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                            Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')
