# Flask
from flask import Blueprint, render_template, session, flash, request
from flask_login import login_required
from flask_api import status

# Security module/library
from markupsafe import escape

# Forms
from forms.message_form import MessageForm

# Service imports
from services.user_service import UserService
from services.message_service import MessageService

from constants import USER_ID, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH, MESSAGE_MIN_LENGTH, MESSAGE_MAX_LENGTH

# Service definitions
us = UserService()
ms = MessageService()


message_page = Blueprint('message_page', __name__,
                        template_folder='templates')

# TODO: Implement
@message_page.route('/', methods=["POST", "GET"])
@login_required
def write_and_get_messages():
    form = MessageForm()

    user_id = session[USER_ID]
    
    # Get messages
    messages = ms.get_messages_by_user_id(user_id)

    
    if form.submit() and request.method == "POST"   :

        if not form.validate():
            return render_template('messages.html', form=form, messages=messages), status.HTTP_400_BAD_REQUEST

        else:
            # extract user inputs from form
            receiver_username = form.receiver.data
            message = form.text.data

            # Get user on username
            user_obj = us.get_user(username=receiver_username)

            if user_obj is not None:
                ms.create_message(sender_id=user_id, receiver_id=user_obj.id, msg=message)
                
                # Added new message, we update the messages variable with the new message included
                messages = ms.get_messages_by_user_id(user_id)

            else:
                # Add escape to the username as this is raw user input.
                flash(f"User with username '{escape(receiver_username)}' does not exist.")
                return render_template('messages.html', form=form, messages=messages), status.HTTP_400_BAD_REQUEST



    return render_template('messages.html', form=form, messages=messages), status.HTTP_200_OK

    
@message_page.route("/messages/from/<int:other_user_id>", methods=['GET', 'POST'])
@login_required
def conversation(other_user_id):
    
    form = MessageForm()
    
    user_id = session[USER_ID]

    other_user_obj = us.get_user_by_id(_id=other_user_id)

    # By default
    conversation = []

    # If user exists
    if other_user_obj is not None:
        if request.method == "POST":
            text = form.text.data
            ms.create_message(sender_id=user_id, receiver_id=other_user_id, msg=text)
        
        # Get the messages (conversation) between the two
        conversation = ms.get_conversation(user_id=user_id, other_user_id=other_user_obj.id)
    
    return render_template("conversation.html", form=form, other_user=other_user_obj, conversation=conversation)