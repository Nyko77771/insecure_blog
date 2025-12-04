from datetime import datetime, timezone
from models.database import DatabaseConnection

class Logger:
    """
    Personal Logging Class that will log details to database.
    """

    # Initialising the Logger class
    def __init__(self):
        try:
            # Creating database connetion
            self.db = DatabaseConnection()
            print('Logger connecting to db')
            self._initialised = True
        except Exception as e:
            print('Logger cant connect to database')
            self._initialised = False

    # Method for checking whether Logger was initialised
    def is_init(self):
        return self._initialised

    # Method for creating and putting logs onto database
    def log(self, action, details, user_id, ip_address = None):
        time = datetime.now(timezone.utc)

        query = "INSERT INTO logs (actionType, user_id, details, ip_address, created_at) VALUES (%s, %s, %s, %s, %s)"
        try:
            self.db.execute_insert_query(query, (action, user_id, details, ip_address, time,))
        except Exception as e:
            print('Log error occurred. Cant log to database')

    # Method for obtaining logs from the database
    def getLogs(self, limit=100):
        query = "SELECT l.*, u.username FROM logs l JOIN users u ON l.user_id = u.id ORDER BY l.created_at DESC LIMIT %s"
        try:
            result = self.db.execute_select_query(query, (limit,))
            if result is not None:
                return result
            else:
                print("No log data")
        except Exception as e:
            print("Could not retrieve logs")
