from models.User import User
from markupsafe import escape

from db.connection import get_db_connection

# Db instance

class UserService:
    def __init__(self):
        self.c = get_db_connection()

    def create_user(self,username:str, password:str):
        self.c.execute(f'''INSERT INTO users (username, password) VALUES(?,?)''', (escape(username),escape(password),))

    def get_user(self, username:str):
        user = self.c.execute(f'''SELECT * FROM users WHERE username == ? ''', (escape(username),)).fetchone()
        if user is None:
            return user
        
        user_obj = User(_id=user[0], username=user[1], password=user[2], isPassHashed=True)

        return user_obj

    def get_user_by_id(self, _id:str):
        user = self.c.execute(f'''SELECT * FROM users WHERE id == ? ''', (escape(_id),)).fetchone()

        if user is None:
            return user

        user_obj = User(_id=user[0], username=user[1], password=user[2])

        return user_obj

    def get_user_ids_from_usernames(self, receiver_id_str:str):
        try:
            user_ids = []
            for username in escape(receiver_id_str).split(","):
                # Fetch user with corresponding username
                user_obj = self.get_user(username)
                # User found -- add the user_id to the list
                if user_obj is not None:
                    user_ids.append(user_obj.id)
            return user_ids
        except:
            return None
