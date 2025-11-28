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
            """
            dotenv_path = join(dirname(__file__), '.env')
            load_dotenv(dotenv_path)
            DATABASE_PASSWORD = os.environ.get("MYSQL_PASSWORD")
            """

            self._connection = mysql.connect(
                host = "localhost",
                user = "root",
                # VULNERABILITY: Sensitive Data Exposure.
                password = "VeryLongANDB0r1nGAns1",
                database = "blog_app"
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
            if params:
                cursor.execute(query,params)
            else:
                # VULNERABILITY: SQL Injection - Query is unparameterized / No params specified. Can be influenced by user
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            print("Query executed. Rows returned: {len(result)}")
            return result
        except Exception as e:
            # VULNERABILITY: Exposes details of an error.
            print(f"Query error: {e}")
            return None

    def execute_insert_query(self,query, params=None):
        if not self._connection:
            print("No active connection")
            return None
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query,params)
            else:
                # VULNERABILITY: SQL Injection - Query is unparameterized / No params specified. Can be influenced by user
                cursor.execute(query)

            self._connection.commit()
            result = cursor.fetchall(size=1)
            cursor.close()
            print(f"Successfully inserted {result['user']}")
            return result
        except Exception as e:
            # VULNERABILITY: Detailed error message.
            print(f"Insert query error: {e}")
            return None

    def execute_update_query(self, query, params=None):
        if not self._connection:
            print("No active connection")
            return None
        try:
            cursor = self._connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                # VULNERABILITY: SQL Injection - Query is unparameterized / No params specified. Can be influenced by user
                cursor.execute(query)

            self._connection.commit()
            result = cursor.fetchall(size=1)
            cursor.close()
            print("Update successful")
            return result
        except Exception as e:
            # VULNERABILITY: Detailed error message.
            print(f"Update error. Error: {e}")

    def close(self):
        if self._connection:
            self._connection.close()
            print("Connection closed")
        DatabaseConnection._instance = None
        DatabaseConnection._connection = None

