from flask import Blueprint
import os


# static_folder=
auth = Blueprint('/auth', __name__,
    static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)),"static"))

# print(auth.static_folder)

from . import views
