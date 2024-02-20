import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()
class Database:

    connection = None

    @classmethod
    def init_connection(cls):
        if not cls.connection:
            cls.connection = mysql.connector.connect(host=os.getenv('HOST'),
                   user=os.getenv('USER'),
                   password='',
                   database=os.getenv('DATABASE'))

        return cls.connection
