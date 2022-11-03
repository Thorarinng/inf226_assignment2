# Apsw 
import apsw
from apsw import Error

c = None

def get_db_connection():
    global c


    # Singleton instance
    if c is not None:
        return c
    
    print("Establishing connection to database..")

    # Only run this when the connection is not established
    try:
        conn = apsw.Connection('./db/tiny.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS announcements (
            id integer PRIMARY KEY, 
            author TEXT NOT NULL,
            text TEXT NOT NULL
            );''')
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id integer PRIMARY KEY, 
            username TEXT NOT NULL,
            password TEXT NOT NULL
            );''')
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
            id integer PRIMARY KEY, 
            message TEXT NOT NULL,
            sender_id integer,
            receiver_id integer,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            CONSTRAINT users

            FOREIGN KEY (sender_id)
            REFERENCES users(sender_id)

            FOREIGN KEY (receiver_id)
            REFERENCES users(receiver_id)
            );''')

        return c
    except Error as e:
        print(e)
        exit()