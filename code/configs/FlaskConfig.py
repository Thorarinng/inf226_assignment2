import os

class FlaskConfig(object):
    # Source to config example: https://medium.com/thedevproject/start-using-env-for-your-flask-project-and-stop-using-environment-variables-for-development-247dc12468be
    # DEBUG = False
    # TESTING = False
    CSRF_ENABLED = True
    SESSION_SECRET = os.environ.get("FLASK_SESSION_SECRET")
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    SESSION_COOKIE_DOMAIN="127.0.0.1:5000"