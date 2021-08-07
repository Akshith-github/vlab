from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and current_user.confirmed:
        if  request.path in ['/auth/login','/auth/','/auth/register','/auth/unconfirmed']:
            flash("User already logged in")
            flash("Log out to visit the authentication page!!")
            return redirect(url_for('main.index'))
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static'\
        and request.path not in ['/auth/unconfirmed','/auth/logout','/auth/confirm']\
        and '/auth/confirm/' not in request.path:
        print(request.path,"\n"*4)
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('unconfirmed.html')



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
        RegistrationFormObj=RegistrationFormObj,slide2="active")
    # return render_template('auth/login.html', form=form)


@auth.route('/login', methods=['GET','POST'])
def login():
    loginFormObj = LoginForm()
    RegistrationFormObj = RegistrationForm()
    if(request.method=='POST'):
        if loginFormObj.validate_on_submit():
            user = User.query.filter_by(email=loginFormObj.email.data.lower()).first()
            if user is not None and user.verify_password(loginFormObj.password.data):
                login_user(user, loginFormObj.remember_me.data)
                next = request.args.get('next')
                print(next,"\n"*8)
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Invalid email or password.')
    return render_template('login.html', loginFormObj=loginFormObj,RegistrationFormObj=RegistrationFormObj,slide2="active")
    # return redirect(url_for('auth.index',loginFormObj=loginFormObj))


@auth.route('/register', methods=['GET','POST'])
def register():
    loginFormObj = LoginForm()
    RegistrationFormObj = RegistrationForm()
    if(request.method=='POST'):
        if RegistrationFormObj.validate_on_submit():
            user = User(email=RegistrationFormObj.email.data.lower(),
                username=RegistrationFormObj.username.data,
                password=RegistrationFormObj.password.data)
            db.session.add(user)
            db.session.commit()
            flash('You can now login to Confirm Your Account')
            token = user.generate_confirmation_token()
            send_email(user.email, 'Confirm Your Account',
                    'mail/confirm', user=user, token=token)
            flash('A confirmation email has been sent to you by email.')
            return redirect(url_for('auth.index'))
        flash("registration failed")
    return render_template('login.html', loginFormObj=loginFormObj,RegistrationFormObj=RegistrationFormObj,
    slide3="active")
    # return redirect(url_for('auth.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.index'))

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
                'mail/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    # input()
    print('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

""" def onLogin(loginFormObj,**kwarg):
    # print(loginFormObj.data)
    user = User.query.filter_by(email=loginFormObj.email.data.lower()).first()
    if user is not None and user.verify_password(loginFormObj.password.data):
        login_user(user, loginFormObj.remember_me.data)
        next = request.args.get('next')
        if next is None or not next.startswith('/'):
            next = url_for('main.index')
        return redirect(next)
    flash('Invalid email or password.')
    return render_template('login.html', loginFormObj=loginFormObj,**kwarg) """

""" def onReg(RegistrationFormObj,**kwarg):
    user = User(email=RegistrationFormObj.email.data.lower(),
            username=RegistrationFormObj.username.data,
            password=RegistrationFormObj.password.data)
    db.session.add(user)
    db.session.commit()
    flash('You can now login.')
    return redirect(url_for('auth.index')) """