# connection.py
import mysql.connector
from mysql.connector import Error


class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='**************',
                database='**********',
                user='**********',
                password='***********'
            )
            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print("server version", db_info)
                self.cursor = self.connection.cursor()
                self.cursor.execute("select database();")
                record = self.cursor.fetchone()
                print("You're connected to database", record)
            else:
                print("Unable to connect")

        except Error as e:
            print("Error while connecting to mysql", e)

        finally:
            if self.connection.is_connected():
                return self.connection

    def close(self):
        try:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("connection closed")
        except Error as e:
            print("Error while closing mysql server connection", e)

        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()
                print("connection closed")
