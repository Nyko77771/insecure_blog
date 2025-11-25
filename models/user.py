from models.database import DatabaseConnection

class User:
    """
    User model
    """

    def __init__(self, username, email, password, role='regular', user_id = None):
        print("Initializing User")
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def db_save(self):
        query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
        db = DatabaseConnection()
        if self.id:
            query = "UPDATE users SET username = %s, email = %s, password = %s, role = %s WHERE id = %s"
        result = db.execute_insert_query

        returned_id = db.execute_insert_query(query, (self.username, self.email, self.password, self.role))

        print(f"New user {self.username} saved with id: {returned_id}")

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users WHERE id = %s"
        db = self._activate_instance()
        results = db.execute_select_query(query,(user_id,))
        if results:
            print("User found by id")
            return results[0]
        else:
            print(f"User by {user_id} not found")
            return None

    def get_all_users(self):
        query = "SELECT id, username, email, role FROM users"
        db = self._activate_instance()
        results = db.execute_select_query(query)
        if results:
            print("User found by id")
            return results
        else:
            print(f"Users not retrieved")
            return None


    def get_user_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        db = self._activate_instance()
        results = db.execute_select_query(query,(username,))
        if results:
            print("User found by username")
            return results[0]
        else:
            print(f"User by {username} not found")
            return None
