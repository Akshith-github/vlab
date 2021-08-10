from flask import render_template, session, request, redirect, url_for, current_app,flash,session,abort
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm
from ..auth.forms import ChangePasswordForm, ChangeEmailForm#, RegistrationForm
from jinja2 import exceptions

# @main.before_app_request
# def before_request():
#     if(not current_user.is_authenticated and request.blueprint==main ):
#         return redirect(url_for('auth.index') )

@main.route('/', methods=['GET'])
@login_required
def index():
    abort(403)
    return render_template('index.html',dir=dir,pageDashboard="active")

@main.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    if("msg" in session):
        flash(session["msg"])
    changePasswordFormObj=ChangePasswordForm()
    changeEmailFormObj=ChangeEmailForm()
    session.pop("msg", None)
    session.pop("chngpwdData", None)
    return render_template('profile.html',pageProfile="active",
        changePasswordFormObj=changePasswordFormObj,
        changeEmailFormObj=changeEmailFormObj)


# @main.route('/<page>', methods=['GET'])
# def renderPage(page):
#     try:
#         return render_template(page,current_user=current_user,RegistrationFormObj=RegistrationForm())
#     except exceptions.TemplateNotFound:
#         abort(404)
#     except:
#         abort(500)