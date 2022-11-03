from collections import UserDict
from email import message
from enum import unique
from heapq import merge
from models.Message import Message
from markupsafe import escape

# Db instance
from db.connection import get_db_connection


class MessageService:
    def __init__(self):
        self.c = get_db_connection()

    def get_messages_by_user_id_and_msg_id(self, user_id:int, msg_id:int):
        messages = self.c.execute(f'''SELECT * FROM messages WHERE (sender_id == ? or receiver_id == ?) and id == ?;''', (escape(user_id),escape(user_id),escape(msg_id),)).fetchone()
        return messages

    def _convert_to_message_type(self,raw_db_message):
        (_id, text,sender_id, receiver_id, timestamp) = raw_db_message
        
        message_obj = Message(_id=_id,text=text, sender_id=sender_id, receiver_id=receiver_id, timestamp=timestamp)

        return message_obj

    def _remove_duplicates(self, merge_lis):
        _dict = {}
        for x in merge_lis:
            _dict[str(x.id)] = x

        unique_lis = list(_dict.values())

        return unique_lis


    def _merge_and_sort(self, messages, other_messages, IsDecending=False):
        merge_lis = messages + other_messages

        unique_lis = self._remove_duplicates(merge_lis=merge_lis)

        unique_lis.sort(key=lambda message: message.timestamp, reverse=IsDecending)

        return unique_lis

    def get_conversation(self, user_id:int, other_user_id:int):
        # Messages sent by session user
        messages = self.c.execute(f'''SELECT * FROM messages WHERE sender_id == ? and receiver_id == ?;''', (escape(user_id),escape(other_user_id),)).fetchall()

        messages_obj = [self._convert_to_message_type(raw_db_message=raw_db_message) for raw_db_message in messages]

        # Messages sent by other user
        other_messages = self.c.execute(f'''SELECT * FROM messages WHERE sender_id == ? and receiver_id == ?;''', (escape(other_user_id),escape(user_id),)).fetchall()

        other_messages_obj = [self._convert_to_message_type(raw_db_message=raw_db_message) for raw_db_message in other_messages]

        # Merge messages sent to a user and from a user - sort by timestamp.
        merge_lis = self._merge_and_sort(messages=messages_obj, other_messages=other_messages_obj)

        return merge_lis

    def create_message(self, sender_id:int, receiver_id:int, msg:str):
        self.c.execute(f'''INSERT INTO messages (message, sender_id, receiver_id) VALUES(?,?,?);''', (escape(msg), escape(sender_id), escape(receiver_id),))

    def get_messages_by_user_id(self, user_id:int):
        messages_sender = self.c.execute(f'''SELECT * FROM messages WHERE sender_id == ?;''', (user_id,)).fetchall()
        messages_receiver = self.c.execute(f'''SELECT * FROM messages WHERE receiver_id == ?;''', (user_id,)).fetchall()

        messages_sender_obj = [self._convert_to_message_type(raw_db_message=raw_db_message) for raw_db_message in messages_sender]
        messages_receiver_obj = [self._convert_to_message_type(raw_db_message=raw_db_message) for raw_db_message in messages_receiver]

        merge_lis = self._merge_and_sort(messages=messages_sender_obj, other_messages=messages_receiver_obj, IsDecending=False)

        return merge_lis
