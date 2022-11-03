# Inbuilt python module
import os

# FLask imports
from flask import Flask, session

# Login Manager
import flask_login

# Flask_wtf CSRF protection
from flask_wtf.csrf import CSRFProtect

# Import routes
from routes.user_routes import user_page
from routes.message_routes import message_page
from api.api import api
from policies.policies import policies

# Get config for flask app
from configs.FlaskConfig import FlaskConfig

# DB
from db.connection import get_db_connection

# constants
from constants import USER_ID

from services.user_service import UserService


def init_csrf_protection():
    # If CSRF protection is enabled in config file
    if fc.CSRF_ENABLED:
        csrf.init_app(app)

def init_login_manager():
    # Add a login manager to the app
    global login_manager
    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)
    # Here we specify the default login view when @login_required fires false - we point the user to user_page.login endpoint
    login_manager.login_view = "user_page.login"

def update_cookie_config():
    print("Cookie config updated!")
    # Set appropriate cookie settings
    app.config.update(
        SESSION_COOKIE_HTTPONLY=fc.SESSION_COOKIE_HTTPONLY,
        SESSION_COOKIE_SECURE=fc.SESSION_COOKIE_SECURE,
        SESSION_COOKIE_SAMESITE=fc.SESSION_COOKIE_SAMESITE,
        SESSION_COOKIE_DOMAIN=fc.SESSION_COOKIE_DOMAIN,

    )

def set_secret_key():
    # The secret key enables storing encrypted session data in a cookie (make a secure random key for this!)
    app.config.update(
        SECRET_KEY=fc.SESSION_SECRET
    )


''' 

Program starts

'''


''' Variable definitions '''

# Fetches settings and configurations for the app, as well as environment variables
fc = FlaskConfig()

# Instantiate user service instance - gives access to methods which have read and write access to the database
us = UserService()

# Establish a singleton database connection
c = get_db_connection()

# Define csrf instance from flas_wtf library
csrf = CSRFProtect()
login_manager = None


''' App Starts '''

# Set up app
app = Flask(__name__)

# Register routes to app
app.register_blueprint(blueprint=user_page)
app.register_blueprint(blueprint=message_page)
app.register_blueprint(blueprint=api)
app.register_blueprint(blueprint=policies)

# Init various components lazyly as defined in the documentation - e.g https://flask-wtf.readthedocs.io/en/1.0.x/csrf/
init_csrf_protection()
init_login_manager()
update_cookie_config()
set_secret_key()


# This method is called whenever the login manager needs to get the User object for a given user id
# The importance of this decorator is important enough to be kept in app.py file, while others are outsourced to various files
@login_manager.user_loader
def user_loader(_id):
    try:
        _id = session[USER_ID]

        if _id is None:
            return False

        user = us.get_user_by_id(_id=_id)

        return user
    except Exception as e:
        return False
