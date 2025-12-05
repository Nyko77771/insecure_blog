from models.database import DatabaseConnection

# User Class
# Performs Methods tied to User
# VULNERABILITY: Missinng hashing method
class User:
    """
    User model
    """

    # Instantiation method for creating new user
    # VULNERABILITY: Password not hashed
    def __init__(self, username, email, password, role='regular', user_id = None):
        print("Initializing User")
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    # Method for saving user details to MySQL
    # VULNERABILITY: Password saved as plain text
    def db_save(self):
        """
        Secure Version:
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
        """
        db = DatabaseConnection()
        if self.id:
            query = f"UPDATE users SET username = {self.username}, email = {self.email}, password = {self.password}, role = {self.password} WHERE id = {self.id}"
            result = db.execute_update_query(query)
            if result:
                print(f"User {self.username} updated")
                return self.id
        else:
            query = f"INSERT INTO users (username, email, password, role) VALUES ({self.username}, {self.email}, {self.password}, {self.role})"

            result = db.execute_insert_query(query)
            if result:
                print(f"New user {self.username} saved with id: {result}")
        return None

    # Method for getting user details from database based on ID
    def get_user_by_id(user_id):
        """
        Secure Version:
           query = "SELECT * FROM users WHERE id = %s"
            db = DatabaseConnection()
        r   esults = db.execute_select_query(   query,(user_id,))
            if results:
                print("User found by id")
                return results[0]
        """
        query = f"SELECT * FROM users WHERE id = {user_id}"
        db = DatabaseConnection()
        results = db.execute_select_query(query)
        if results:
            print("User found by id")
            return results[0]
        else:
            # VULNERABILITY: Too much information provided.
            print(f"User by {user_id} not found")
            return None

    # Method for getting all users from database
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


    # Method for getting user details from database based on username given
    def get_user_by_username(username):
        """
        Secure Version:
            query = "SELECT * FROM users WHERE username = %s"
            db = DatabaseConnection()
            results = db.execute_select_query(query,(username,))
        """
        # VULNERABILITY: Un-parameterized query
        query = f"SELECT * FROM users WHERE username = '{username}"
        db = DatabaseConnection()
        results = db.execute_select_query(query)
        if results:
            # VULNERABILITY: Too much information provided.
            print(f"User found by username. User {results}")
            return results[0]
        else:
            print(f"User by {username} not found")
            return None

    # Method for getting user details from database based on email
    def get_user_by_email(email):
        """
        Secure Version:
            query = "SELECT * FROM users WHERE email = %s"
            db = DatabaseConnection()
            results = db.execute_select_query(query,(email,))

        """
        # VULNERABILITY: Un-parameterized query
        query = f"SELECT * FROM users WHERE email = '{email}'"
        db = DatabaseConnection()
        results = db.execute_select_query(query)
        if results:
            print("User found by email")
            return results[0]
        else:
            # VULNERABILITY: Too much information provided.
            print(f"User by {email} not found")
            return None

    # Method for removing user details from database
    def delete_user(self):
        """
        Secure Version:
            if self.id is None:
                print("No ID found. User cant be deleted")
                return None
            db = DatabaseConnection()
            query = "DELETE FROM users WHERE id = %s"
            result = db.execute_update_query(query, (self.id))
        """
        if self.id is None:
            print("No ID found. User cant be deleted")
            return None
        db = DatabaseConnection()
        query = f"DELETE FROM users WHERE id = {self.id}"
        result = db.execute_update_query(query)
        if result:
            # VULNERABILITY: Too much information provided.
            print(f"User {self.username} has been removed")
            print(f"Result returned: {result}")
            return result
        return None

    # Method for authenticating new users
    # VULNERABILITY: Plain password comparison
    def authenticate(username, password):
        try:
            # VULNERABILITY: Un-parameterized query
            db = DatabaseConnection()
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

            results = db.execute_select_query(query)
            if results:
                user = results[0]
                return User(user_id = user[0], username = user[1], email = user[2], password = user[3], role = user[4])
            else:
                print(f"User {username} failed to validate")
                return None
        except Exception as e:
            print(f"Authentication error occure. Error: {e}")
            return None

    # Method for obtaining new password
    # VULNERABILITY: Password retrieving method is public
    def get_user_password(username):
        """
        Secure Version:
            query = "SELECT password FROM users WHERE username = %s"
            db = DatabaseConnection()
            found_password = db.execute_select_query(query,(username,))
        """
        query = f"SELECT password FROM users WHERE username = {username}"
        db = DatabaseConnection()
        found_password = db.execute_select_query(query)
        if found_password:
            # VULNERABILITY: Too much information provided.
            print(f"User password found. Password: {found_password}")
            return found_password[0]
        else:
            # VULNERABILITY: Too much information provided.
            print(f"User by {username} not found when looking for pasword")
            return None

    # Method for defining key value pairs for the user class
    def create_key_pair(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role
        }
