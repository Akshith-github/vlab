from flask import render_template, session, request, redirect, url_for, current_app,flash,session,abort
from flask_login import login_user, logout_user, login_required, current_user
from .. import db
from ..models import User,Role
from ..email import send_email
from . import course
from ..auth.forms import ChangePasswordForm, ChangeEmailForm#, RegistrationForm
from jinja2 import exceptions

# @course.before_app_request
# def before_request():
#     if(not current_user.is_authenticated and request.blueprint==course ):
#         return redirect(url_for('auth.index') )

@course.route('/all', methods=['GET'])
def index():
    print("course staic url",course.static_url_path)
    # abort(500)
    return render_template('courses.html',pagecourses="active")

@course.route("/<courseCode>",methods=['GET'])
def render_course(courseCode):
    if(not courseCode):
        return redirect(url_for('course.index'))
    print("rendering course code:",courseCode)
    if(courseCode not in ["CSE18R123","CSE18R456","CSE18R789","CSE18R890"]):
        abort(404)
    if(courseCode not in ["CSE18R123","CSE18R456"]):
        return render_template("CourseIntro.html",pagecourseIntro="active")
    return render_template("EnrolledCourse.html",pageEnrolledcourse="active")

@course.route("/workbench",methods=['GET'])
@login_required
def render_course_workbench():
    if(current_user.role == Role.query.filter_by(name='Student').first()):
        abort(403)
    return render_template("cabin.html",pageCabin="active")

@course.route("/<courseCode>/teacherlog",methods=['GET'])
@login_required
def render_teacher_course_log(courseCode):
    if(current_user.role == Role.query.filter_by(name='Student').first()):
        abort(403)
    if(courseCode not in ["CSE18R123","CSE18R456","CSE18R789","CSE18R890"]):
        abort(404)
    return render_template("TchrCrsDash.html")