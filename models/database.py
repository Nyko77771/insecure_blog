import mysql.connector as mysql
import os
from os.path import join, dirname
from dotenv import load_dotenv

class DatabaseConnection:
    """
    Singleton class
    Used for establishing and managing Database Connections
    """
    _instance = None # internal variable for instance tracking
    _connection = None # internal variable for connection tracking


    # Method for creating an instance
    def __new__(cls):
        if cls._instance is None: #If no instance
            cls._instance = super(DatabaseConnection, cls).__new__(cls)#Creating new instance
            cls._instance._init_connection()
        return cls._instance #return same instance

    def _init_connection(self):
        try:

            dotenv_path = join(dirname(__file__), '.env')
            load_dotenv(dotenv_path)
            DATABASE_PASSWORD = os.environ.get("MYSQL_PASSWORD")
            DATABASE_HOST = os.environ.get("MYSQL_HOST")
            DATABASE_USER = os.environ.get("MYSQL_USER")
            DATABASE= os.environ.get("MYSQL_DATABASE")

            self._connection = mysql.connect(
                host = DATABASE_HOST,
                user = DATABASE_USER,
                password = DATABASE_PASSWORD,
                database = DATABASE
            )

            print("MySQL connection established")
        except Exception as e:
            print(f"Failed to connect to MySQL. Error: {e}")
            self._connection = None

    def get_connection(self):
        return self._connection

    def execute_select_query(self,query,params=None):
        if not self._connection:
            print("No active connection")
            return None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query,params)
            result = cursor.fetchall()
            cursor.close()
            print("Query executed. Rows returned: {len(result)}")
            return result
        except Exception as e:
            print(f"SELECT query execution failed.")
            return None

    def execute_insert_query(self,query, params=None):
        if not self._connection:
            print("No active connection")
            return None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query,params)
            self._connection.commit()
            result_id = cursor.lastrowid
            cursor.close()
            print(f"Successfully inserted {result_id}")
            return result_id
        except Exception as e:
            print(f"Insert query execution failed")
            return None

    def execute_update_query(self, query, params=None):
        if not self._connection:
            print("No active connection")
            return None
        try:
            cursor = self._connection.cursor()
            cursor.execute(query, params)
            self._connection.commit()
            result_id = cursor.lastrowid
            cursor.close()
            print("Update successful")
            return result_id
        except Exception as e:
            # VULNERABILITY: Detailed error message.
            print(f"Update execution error occured.")

    def close(self):
        if self._connection:
            self._connection.close()
            print("Connection closed")
        DatabaseConnection._instance = None
        DatabaseConnection._connection = None

