"""
Data Layer: Saves a message into the 'nats_messages_db' table of the PostgreSQL database.
"""

import psycopg2
from datetime import datetime

def save_message(content: str):
    """
    Saves a message into the 'nats_messages_db' table of the PostgreSQL database.

    Parameters:
    ----------
    content : str
        The textual content of the message to be stored in the database.

    Functionality:
    -------------
    - Connects to the PostgreSQL database 'nats_messages_db'
    - Inserts the provided message content along with the current timestamp
    - Commits the transaction and closes the connection

    Logs:
    -----
    - Prints confirmation if successful
    - Prints error message if an exception occurs
    """
    try:
        # Connect to my PostgreSQL database
        conn = psycopg2.connect(
            dbname="nats_messages_db",
            user="postgres",              
            password="dav13*",            
            host="localhost",
            port="5432"
        )

        # Cursor to perform database operations
        cur = conn.cursor()

        # SQL query to insert message content and current timestamp
        insert_query = """
            INSERT INTO messages (content, timestamp)
            VALUES (%s, %s)
        """
        cur.execute(insert_query, (content, datetime.now()))

        # Commit the transaction
        conn.commit()

        # Close the communication with the database
        cur.close()
        conn.close()

        print(f"[DB] Message saved: {content}")

    except Exception as e:
        print("[DB] Error saving message:", e)