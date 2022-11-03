# Flask
from flask import Blueprint, session, jsonify, request
from flask_login import login_required

# Cosntants
from constants import USER_ID

# Services used
from services.user_service import UserService
from services.message_service import MessageService

# Security module/library
from markupsafe import escape

# Define services
us = UserService()
ms = MessageService()

# Define api app blueprint
api = Blueprint('api', __name__)

prefix = "/api"

'''
API ENDPOINTS
'''

# TODO: Implement
@api.post(f'{prefix}/new')
@login_required
def send_message():
    user_id = session[USER_ID]

    # TODO: Retrieve request params
    message, receiver_id = request.get_json().values()

    print(message, receiver_id)

    # Get user on username
    user_obj = us.get_user_by_id(_id=receiver_id)

    if user_obj is not None:
        ms.create_message(sender_id=user_id, receiver_id=user_obj.id, msg=message)

    return jsonify(success=True)

@api.route(f'{prefix}/messages', methods=['POST','GET'])
@login_required
def messages():
    user_id = session[USER_ID]

    messages_obj = ms.get_messages_by_user_id(user_id)

    # Cannot return python class objects - must return application/json
    messages = [(m.id, m.sender_id, m.receiver_id, m.text, m.timestamp) for m in messages_obj]

    return messages

# TODO: Implement
@api.get(f'{prefix}/messages/<int:msg_id>')
@login_required
def get_message_by_msg_id(msg_id):
    user_id = session[USER_ID]
    messages = ms.get_messages_by_user_id_and_msg_id(user_id=user_id, msg_id=escape(msg_id))
    return [messages]
