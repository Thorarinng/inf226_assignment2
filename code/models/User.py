import flask_login
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape

# Class to store user info
# UserMixin provides us with an `id` field and the necessary
# methods (`is_authenticated`, `is_active`, `is_anonymous` and `get_id()`)
class User(flask_login.UserMixin):
    def __init__(self, _id, username, password, isPassHashed=False) -> None:
        self.id = _id
        self.username = escape(username)

        # When creating new users we generate a hashed password
        if not isPassHashed:
            self.password_hash = self.generate_password_hash(escape(password))
        # When simply creating a user object we do not want to rehash the password
        else:
            self.password_hash = password

    def generate_password_hash(self, password:str) -> str:
        '''
        Method used when creating new user and assigning a hashed representation of the password
        - Used for register and login
        - Returns str - hash of password
        '''
        return generate_password_hash(password)

    def verify_password(self, password:str) -> str:
        '''
        Verifying that the hash of the given password matches the current password hash
        - Used for login
        - Returns boolean: True or False
        '''
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f'''\n
        id: {self.id}
        username: {self.username}
        password_hash: {self.password_hash}\n
        '''
