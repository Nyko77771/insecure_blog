from models.database import DatabaseConnection
import bcrypt

# User Class
# Performs Methods tied to User
# Secure Version
# Fixed Un-parameterized queries
# Removed Generic Comments
class User:
    """
    User model
    """

    # Instantiation method for creating new user
    def __init__(self, username, email, password, role='regular', user_id = None, salt = None):
        print("Initializing User")
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    # Method for saving user details to MySQL
    def db_save(self):
        db = DatabaseConnection()
        hashed_password = self._hash_password(self.password)
        if self.id:

            query_update = "UPDATE users SET username = %s, email = %s, password = %s, role = %s WHERE id = %s"

            result = db.execute_update_query(query_update, (self.username, self.email, hashed_password, self.role, self.id))
            if result:
                print("User details updated")
        else:

            query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"

            result = db.execute_insert_query(query, (self.username, self.email, hashed_password, self.role))
            if result:
                print(f"New user saved.")

    # Method for hashing password
    @staticmethod
    def _hash_password(password):
        bytes = str(password).encode('utf-8')
        salt = bcrypt.gensalt(12)
        hash = bcrypt.hashpw(bytes, salt)
        print('Hashed Password')
        return hash.decode()

    # Method for checking password
    @staticmethod
    def verify_password(new_password, stored_password):
        print("Veryfying passwords")
        new_bytes = str(new_password).encode('utf-8')
        if isinstance(stored_password, str):
            stored_bytes = stored_password.encode('utf-8')
        else:
            stored_bytes = stored_password
        print(f"Retrieved: {stored_bytes}, New {new_bytes}")
        result = bcrypt.checkpw(new_bytes, stored_bytes)
        print("Match")
        return result

    # Method for getting user details from database based on ID
    def get_user_by_id(user_id):
        query = "SELECT * FROM users WHERE id = %s"
        db = DatabaseConnection()
        results = db.execute_select_query( query,(user_id,))
        if results:
            print("User found by id")
            return results[0]
        else:
            print(f"User not found")
            return None

    # Method for getting all users from database
    def get_all_users():
        query = "SELECT id, username, email, role FROM users"
        db = DatabaseConnection()
        results = db.execute_select_query(query)
        if results:
            print("Users found")
            return results
        else:
            print(f"Users not retrieved")
            return None

    # Method for getting user details from database based on username given
    def get_user_by_username(username):
        query = "SELECT * FROM users WHERE username = %s"
        db = DatabaseConnection()
        results = db.execute_select_query(query,(username,))
        if results:
            print(f"Data found: {results[0]}")
            return results[0][0]
        else:
            print("Not found")
            return None

    # Method for getting user details from database based on email
    def get_user_by_email(email):
        query = "SELECT * FROM users WHERE email = %s"
        db = DatabaseConnection()
        results = db.execute_select_query(query,(email,))
        if results:
            print("Data found")
            return results[0]
        else:
            print("Not found")
            return None

    # Method for removing user details from database
    def delete_user(self):
        if self.id is None:
            print("No ID found.")
            return None
        db = DatabaseConnection()
        query = "DELETE FROM users WHERE id = %s"
        result = db.execute_update_query(query, (self.id))
        if result:
            print(f"Data has been removed")
            return result
        return None

    # Method for authenticating new users
    @classmethod
    def authenticate(self, username, password):
        try:

            retrieved_list = self._get_password(username)
            if not retrieved_list:
                print("Nothing found")
                return None
            retrieved_password = retrieved_list[0][0]

            performed_comparison = self.verify_password(password, retrieved_password)

            if performed_comparison:
                db = DatabaseConnection()
                query = "SELECT * FROM users WHERE username = %s AND password = %s"

                results = db.execute_select_query(query, (username, retrieved_password,))
                if results:
                    user = results[0]
                    return User(user_id = user[0], username = user[1], email = user[2], password = user[3], role = user[4])
                else:
                    print("Failed to validate")
                    return None
        except Exception as e:
            print(f"Authentication error occured. Error {e}")
            return None

    # Method for retrieving password
    def _get_password(username):
        query = "SELECT password FROM users WHERE username = %s"
        db = DatabaseConnection()
        results = db.execute_select_query(query,(username,))
        if results:
            print("Data found")
            return results
        else:
            print("Not found")
            return None



    # Method for defining key value pairs for the user class
    def create_key_pair(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
