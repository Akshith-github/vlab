import os
import click
from flask import abort,redirect,url_for
from flask_migrate import Migrate, upgrade
from app import create_app, db
from app.models import User, Role
from dotenv import load_dotenv
from flask_admin.contrib import sqla
from flask_login import login_user, logout_user, login_required, current_user

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
# print(os.environ)
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

from flask_admin import Admin , AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin import helpers, expose


class MyModelView(sqla.ModelView):

    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        abort(403)

class MyAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if current_user.is_authenticated and \
            current_user.role==Role.query.filter_by(name='Admin').first():
            return super(MyAdminIndexView, self).index()
        return abort(403)
admin = Admin(app,index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    """Run the unit tests."""
    import unittest
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()