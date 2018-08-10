"""
web handlers
"""
#pylint: disable=import-error
from flask import Flask, request
import jrg.util
import jrg.setup

from google.appengine.api import users

APP = Flask(__name__)

jrg.setup.setup(APP)

@APP.route('/auth/admin-user')
def root():
    user = users.get_current_user()
    return_path = request.args['return']

    rv = dict()
    if user:
        rv['logoutUrl'] = users.CreateLogoutURL(return_path)
        rv['loggedIn'] = True
        rv['user'] = user
        rv['admin'] = users.is_current_user_admin()

    else:
        rv['loginUrl'] = users.create_login_url(return_path)
        rv['loggedIn'] = False

    return jrg.util.to_json(rv)
