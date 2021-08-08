from flask import render_template, redirect, request, url_for, flash,get_flashed_messages,session
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db,flash2
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm,\
    PasswordResetRequestForm, PasswordResetForm, ChangeEmailForm

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and current_user.confirmed:
        if  request.path in ['/auth/login','/auth/','/auth/register','/auth/unconfirmed']:
            flash2("User already logged in")
            flash("User already logged in")
            flash2("Log out to visit the authentication page!!")
            return redirect(url_for('main.index'))
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint \
        and request.blueprint != 'auth' \
        and request.endpoint != 'static'\
        and request.path not in ['/auth/unconfirmed','/auth/logout','/auth/confirm']\
        and '/auth/confirm/' not in request.path:
        # print(request.path,"\n"*4)
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
        RegistrationFormObj=RegistrationFormObj,slide2="active",passwordResetRequestFormObj = PasswordResetRequestForm())
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
                # print(next,"\n"*8)
                if next is None or not next.startswith('/'):
                    next = url_for('main.index')
                return redirect(next)
            flash('Invalid email or password.')
    return render_template('login.html', loginFormObj=loginFormObj,RegistrationFormObj=RegistrationFormObj,slide2="active",passwordResetRequestFormObj = PasswordResetRequestForm())
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
            flash2('A confirmation email has been sent to you by email.')
            return redirect(url_for('auth.index'))
        flash("registration failed")
    return render_template('login.html', loginFormObj=loginFormObj,RegistrationFormObj=RegistrationFormObj,
    slide3="active",passwordResetRequestFormObj = PasswordResetRequestForm())
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

@auth.route('/change-password', methods=['POST'])
@login_required
def change_password():
    changePasswordFormObj = ChangePasswordForm()
    msgs=""
    if changePasswordFormObj.validate_on_submit():
        if current_user.verify_password(changePasswordFormObj.old_password.data):
            current_user.password = changePasswordFormObj.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            # msgs='Your password has been updated.'
            # return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
            # msgs='Invalid password.'
    # for msg in get_flashed_messages():
        # msgs+="\n"+msg
    # session['msg']=msgs
    else:
        flash("failed to change password!! try again !!")
    return redirect(url_for("main.profile"))


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    passwordResetRequestFormObj = PasswordResetRequestForm()
    loginFormObj = LoginForm()
    RegistrationFormObj = RegistrationForm()
    if passwordResetRequestFormObj.validate_on_submit():
        user = User.query.filter_by(email=passwordResetRequestFormObj.email.data.lower()).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'mail/reset_password',
                       user=user, token=token)
        flash('An email with instructions to reset your password has been '
            'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('login.html', passwordResetRequestFormObj=passwordResetRequestFormObj,slide1="active",\
        RegistrationFormObj=RegistrationFormObj,loginFormObj=loginFormObj)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    passwordResetFormObj=PasswordResetForm()
    if passwordResetFormObj.validate_on_submit():
        if User.reset_password(token, passwordResetFormObj.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('reset-password.html',passwordResetFormObj=passwordResetFormObj)


@auth.route('/change_email', methods=['POST'])
@login_required
def change_email_request():
    changeEmailFormObj = ChangeEmailForm()
    if changeEmailFormObj.validate_on_submit():
        if current_user.verify_password(changeEmailFormObj.password.data):
            new_email = changeEmailFormObj.email.data.lower()
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                        'mail/change_email',
                        user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                    'address has been sent to you.')
            # return redirect(url_for('main.profile'))
        else:
            flash('Invalid email or password.')
    return redirect(url_for('main.profile'))
    # return render_template("profile.html", changeEmailFormObj=changeEmailFormObj)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
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