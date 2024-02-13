import mysql.connector

class Database:

    connection = None

    @classmethod
    def init_connection(cls):
        if not cls.connection:
            cls.connection = mysql.connector.connect(host='localhost',
                   user='root',
                   password='',
                   database='library')

        return cls.connection
