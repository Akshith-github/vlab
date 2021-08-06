from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm


@auth.route('/', methods=['GET', 'POST'])
def login():
    loginFormObj = LoginForm()
    print(loginFormObj.validate_on_submit())
    if loginFormObj.validate_on_submit():
        print(loginFormObj.data)
        user = User.query.filter_by(email=loginFormObj.email.data.lower()).first()
        if user is not None and user.verify_password(loginFormObj.password.data):
            login_user(user, loginFormObj.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid email or password.')
    return render_template('login.html', loginFormObj=loginFormObj)
    # return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
