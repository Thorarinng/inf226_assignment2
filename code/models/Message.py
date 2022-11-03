import flask_login
from markupsafe import escape

# Class to store user info
# UserMixin provides us with an `id` field and the necessary
# methods (`is_authenticated`, `is_active`, `is_anonymous` and `get_id()`)
class Message(flask_login.UserMixin):
    def __init__(self, _id, sender_id, receiver_id, text, timestamp) -> None:
        self.id = _id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.text = escape(text)
        self.timestamp = timestamp

    def __str__(self):
        return f'''\n
        id: {self.id}
        sender_id: {self.sender_id}
        receiver_id: {self.receiver_id}
        text: {self.text}
        text: {self.timestamp}\n
        '''
