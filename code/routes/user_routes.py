# Flask
from flask import Blueprint, render_template, redirect, session, flash, request
from flask_login import logout_user, login_user, login_required
from flask_api import status

# Security module/library
from markupsafe import escape

# Forms
from forms.login_form import LoginForm
from forms.logout_form import LogoutForm
from forms.register_form import RegisterForm

# Service imports
from services.user_service import UserService
from services.message_service import MessageService

# Model imports
from models.User import User

# CONSTANTS
from constants import USER_ID

# Service definitions
us = UserService()
ms = MessageService()

user_page = Blueprint('user_page', __name__,
                        template_folder='templates')

@user_page.route('/logout', methods=['POST','GET'])
@login_required
def logout():
    form = LogoutForm()
    if form.is_submitted():
        # This also cleans up the remember me cookie if it exists
        logout_user()
        return redirect("/login")
    return render_template('./logout.html', form=form)


# TODO: Implement
@user_page.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if not form.validate_on_submit() and request.method == "POST":
        return render_template('./login.html', form=form), status.HTTP_400_BAD_REQUEST

    if form.validate_on_submit() and request.method == 'POST':
        # extract user inputs from form
        username = form.username.data
        password = form.password.data

        # Get user on username
        user_obj = us.get_user(username=username)

        if user_obj is None:
            flash(f"User with username '{escape(username)}' does not exist.")
            return render_template('./login.html', form=form), status.HTTP_400_BAD_REQUEST
            
        
        elif not user_obj.verify_password(password=password):
            flash(f"Wrong password.")
            return render_template('./login.html', form=form), status.HTTP_400_BAD_REQUEST

        else:
            login_user(user_obj)
            # Insert user into session with key=_id
            session[USER_ID] = user_obj.id

            return redirect("/")

    return render_template('./login.html', form=form)

@user_page.route("/register", methods=["POST","GET"])
def register():
    form = RegisterForm()

    if not form.is_submitted():
        return render_template('./register.html', form=form)

    if request.method == "POST":

        if not form.validate_on_submit():
            return render_template('./register.html', form=form), status.HTTP_400_BAD_REQUEST



        username = form.username.data
        password1 = form.password1.data
        password2 = form.password2.data


        if password1 != password2:
            flash("Passwords do not match")
            return render_template('./register.html', form=form), status.HTTP_400_BAD_REQUEST

        
        else:
            user_obj = us.get_user(username=username)

            # User not found - create a new user
            if user_obj is None:
                # Instantiate instance to calculate encrypted hash of password 
                user_obj = User(_id=None, username=username, password=password1)
                # Create the user
                us.create_user(username=user_obj.username, password=user_obj.password_hash)
                # Get the user again to obtain the id
                user_obj = us.get_user(username=username)
                # Insert user into session with key=_id
                session[USER_ID] = user_obj.id
                # Log the user in
                login_user(user_obj)
                # Redirect to base
                return redirect("/")
            else:
                flash(f"User with {escape(user_obj.username)} already exists")


    return render_template('./register.html', form=form)
