from datetime import datetime
from models.database import DatabaseConnection

class Blog():
    def __init__(self, user_id, title, content, post_id=None):
        self.id = post_id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.update_at = datetime.now()
        return None

    def db_save(self):
        db = DatabaseConnection()
        query = "INSERT INTO blogs (user_id, title, content, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)"
        try:
            result = db.execute_insert_query(query, (self.user_id, self.title, self.content, self.created_at, self.update_at))
            print(f"New created blog: {result}")
            blog_id = result
            if blog_id:
                print(f"New blog inserted. Id: {blog_id}")
                self.id = blog_id
                return blog_id
            else:
                # VULNERABILITY: Too much information is given.
                print(f"Unable to save blog. Blog ID is missing.")
                return None
        except Exception as e:
            # VULNERABILITY: Too much information is given.
            print(f"An exception occured. Error: {e}")
            return None


    def update(self):
        self.update_at = datetime.now()
        db = DatabaseConnection()
        query = "UPDATE posts SET title = %s, content = %s, update_at = %s"
        try:
            result = db.execute_update_query(query, (self.title, self.content, self.update_at,))
            if result:
                print(f"Blog ID: {self.id} updated at {result["update_at"]}")
                return True
        except Exception as e:
            # VULNERABILITY: Too much information is given.
            print(f"An exception occured. Error: {e}")
            return False

    def delete(blog_id):
        db = DatabaseConnection()
        query = "DELETE FROM posts WHERE id = %s"
        try:
            result = db.execute_update_query(query, (blog_id,))
            print(f"Blog Id {result['id']} deleted.")
            return True
        except Exception as e:
            # VULNERABILITY: Too much information is given.
            print("An exception occured. Error: {e}")
            return False

    def get_all_user_blogs(username):
        db = DatabaseConnection()
        query = "SELECT b.id, b.title, u.username FROM blogs b JOIN users u ON b.user_id = u.id WHERE u.username = %s ORDER BY b.created_at DESC"

        try:
            result = db.execute_select_query(query, (username,))
            # VULNERABILITY: Too much information
            if result:
                print(f"All user blogs retrieved.")
                return result
            else:
                print("No blogs returned")
                return None
        except Exception as e:
            # VULNERABILITY: Too much information is given.
            print("An exception occured. Error: {e}")
            return None

    def get_blog_by_id(search_id):
        db = DatabaseConnection()
        query = "SELECT b.title, u.username, b.content FROM blogs b JOIN users u on b.user_id = u.id WHERE b.id = %s"
        try:
            result = db.execute_select_query(query, (search_id,))
            if result:
                print(f"Found blog by id. Result: {result}")
                return result
            else:
                print(f"Blog is not found by given id")
                return None
        except Exception as e:
            # VULNERABILITY: Too much information is given.
            print("An exception occured. Error: {e}")
            return None

    def search(search_word):
        """
        Secure Version:
            db = DatabaseConnection()
            query = "SELECT b.id, b.title, u.username FROM blogs b JOIN users u ON b.user_id = u.id WHERE b.title LIKE %s"
            try:
                pattern = "%" + search_word + "%"
                result = db.execute_select_query(query, (pattern,))

        """
        db = DatabaseConnection()
        query = "SELECT * FROM blogs b JOIN users u ON b.user_id = u.id WHERE b.title LIKE %s"
        try:
            pattern = f"%{search_word}%"
            result = db.execute_select_query(query, (pattern,))
            if result:
                print(f"Search items found. Result: {result}")
                return result
            else:
                print("Search did not find anything")
                return None
        except Exception as e:
            # VULNERABILITY: Too much information is given.
            print("An exception occured. Error: {e}")
            return None





