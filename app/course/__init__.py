from flask import Blueprint,url_for
import os


# static_folder=
course = Blueprint('course', __name__,
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)),"static"))

# print(auth.static_folder)

from . import views
