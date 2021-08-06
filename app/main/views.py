from flask import render_template, session, request, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User
from ..email import send_email
from . import main
from .forms import NameForm

# @main.before_app_request
# def before_request():
#     if(not current_user.is_authenticated and request.blueprint==main ):
#         return redirect(url_for('auth.index') )

@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('index.html',dir=dir,pageDashboard="active")

@main.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html',pageProfile="active")


# @main.route('/<page>', methods=['GET'])
# def renderPage(page):
#     return render_template(page,current_user=current_user)