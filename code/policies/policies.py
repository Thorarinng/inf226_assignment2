# from flask
from flask import Blueprint

# Define api app blueprint
policies = Blueprint('policies', __name__)

@policies.after_request
def add_security_headers(resp):
    # Source: https://stackoverflow.com/questions/63290047/flask-csp-content-security-policy-best-practice-against-attack-such-as-cross
    #  Source: https://smirnov-am.github.io/securing-flask-web-applications/
    '''
    The following content security policy instructs the browser to load and execute scripts from the same source - your server, whic is identified by protocol (http/https)
    , hostname and port triplet. It also disabled inline scripts like we can get from malicious code.
    '''
    resp.headers['Content-Security-Policy']='default-src \'self\''
    return resp
