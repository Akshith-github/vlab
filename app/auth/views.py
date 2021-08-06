from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm

def onLogin(loginFormObj,**kwarg):
    # print(loginFormObj.data)
    user = User.query.filter_by(email=loginFormObj.email.data.lower()).first()
    if user is not None and user.verify_password(loginFormObj.password.data):
        login_user(user, loginFormObj.remember_me.data)
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('main.index')
        return redirect(next)
    flash('Invalid email or password.')
    return render_template('login.html', loginFormObj=loginFormObj,**kwarg)

def onReg(RegistrationFormObj,**kwarg):
    user = User(email=RegistrationFormObj.email.data.lower(),
            username=RegistrationFormObj.username.data,
            password=RegistrationFormObj.password.data)
    db.session.add(user)
    db.session.commit()
    flash('You can now login.')
    return redirect(url_for('/auth.index'))

@auth.route('/', methods=['GET','POST'])
def index(loginFormObj=None):
    if(not loginFormObj):
        loginFormObj = LoginForm()
    RegistrationFormObj = RegistrationForm()
    # print(dir(RegistrationFormObj.username))
    # print(loginFormObj.validate_on_submit())
    """ if loginFormObj.validate_on_submit():
        return onLogin(loginFormObj,RegistrationFormObj=RegistrationFormObj)
    if RegistrationFormObj.validate_on_submit():
        return onReg(RegistrationFormObj,loginFormObj=loginFormObj) """
    return render_template('login.html', loginFormObj=loginFormObj,
        RegistrationFormObj=RegistrationFormObj)
    # return render_template('auth/login.html', form=form)


@auth.route('/login', methods=['POST'])
def login():
    loginFormObj = LoginForm()
    RegistrationFormObj = RegistrationForm()
    if loginFormObj.validate_on_submit():
        user = User.query.filter_by(email=loginFormObj.email.data.lower()).first()
        if user is not None and user.verify_password(loginFormObj.password.data):
            login_user(user, loginFormObj.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('login.html', loginFormObj=loginFormObj,RegistrationFormObj=RegistrationFormObj)
    # return redirect(url_for('/auth.index',loginFormObj=loginFormObj))


@auth.route('/register', methods=['POST'])
def register():
    loginFormObj = LoginForm()
    RegistrationFormObj = RegistrationForm()
    if RegistrationFormObj.validate_on_submit():
        return onReg(RegistrationFormObj,loginFormObj=loginFormObj) 
    return redirect(url_for('/auth.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('/auth.index'))
