from models.database import DatabaseConnection

# VULNERABILITY: Missinng hashing method
class User:
    """
    User model
    """

    # VULNERABILITY: Password not hashed
    def __init__(self, username, email, password, role='regular', user_id = None):
        print("Initializing User")
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    # VULNERABILITY: Password saved as plain text
    def db_save(self):
        db = DatabaseConnection()
        if self.id:
            query = "UPDATE users SET username = %s, email = %s, password = %s, role = %s WHERE id = %s"
            result = db.execute_update_query(query, (self.username,
            self.email,
            self.password,  #VULNERABILITY: Storing plaintext
            self.role,
            self.id))
            if result:
                print(f"User {self.username} updated")
                return self.id
        else:
            query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"

            result = db.execute_insert_query(query, (self.username, self.email, self.password, self.role))
            if result:
                print(f"New user {self.username} saved with id: {result}")
        return None

    def get_user_by_id(user_id):
        query = "SELECT * FROM users WHERE id = %s"
        db = DatabaseConnection()
        results = db.execute_select_query(query,(user_id,))
        if results:
            print("User found by id")
            return results[0]
        else:
            print(f"User by {user_id} not found")
            return None

    def get_all_users():
        query = "SELECT id, username, email, role FROM users"
        db = DatabaseConnection()
        results = db.execute_select_query(query)
        if results:
            print("User found by id")
            return results
        else:
            print(f"Users not retrieved")
            return None


    def get_user_by_username(username):
        query = "SELECT * FROM users WHERE username = %s"
        db = DatabaseConnection()
        results = db.execute_select_query(query,(username,))
        if results:
            print("User found by username")
            return results[0]
        else:
            print(f"User by {username} not found")
            return None

    def delete_user(self):
        if self.id is None:
            print("No ID found. User cant be deleted")
            return None
        db = DatabaseConnection()
        query = "DELETE FROM users WHERE id = %s"
        result = db.execute_update_query(query, (self.id))
        if result:
            print(f"User {self.username} has been removed")
            print(f"Result returned: {result}")
            return result
        return None

    # VULNERABILITY: Plain password comparison
    def authenticate(username, password):
        try:
            user = User.get_user_by_username(username)
            print(f"returned user: {user}")
            user_password = user['password']
            if user and user_password == password:
                print(f"User {username} is validated")
                return user
            else:
                print(f"User {username} failed to validate")
                return None
        except Exception as e:
            print(f"Authentication error occure. Error: {e}")
            return None


