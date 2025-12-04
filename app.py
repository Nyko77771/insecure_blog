# importing flask methods
from flask import Flask, render_template, request, session, redirect, flash
# Importing flask-talisman for secure headers management
from flask_talisman import Talisman
# Imporing dotenv library for accessing dotenv variables
from dotenv import load_dotenv
# Importing datetime's timedelta method for time manipulation
from datetime import timedelta
# Library for finding path to files
from os.path import dirname, join
import os
# Importing my models:
from models.user import User
from models.blogs import Blog
from models.events import EventLogger


# Creating flask instance
app = Flask(__name__)
# Making an alias for render function
render = render_template
# Creating talisman variable
talisman = Talisman(app)

# Specifying env path for obtaining the env variable
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# Assigning secret
app.secret_key = os.environ.get("FLASK_SECRET")
# Setting up a debugging enviroment
app.config["DEBUG"] = True
# Creating a timeout time for session
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=20)


# Configuring Talisman
"""
    1)X-XSS-Protection,
    2)Strict-Transport-Security,
    3)Content-Security-Policy
"""
# Defining Content Security Policy
# Telling the browser to load resources that are of the same origin.
# Used to prevent XSS
csp = {"default-src": "'self'",
       "img-src": '*',
       "style-src": [ "'self'", "https://cdn.jsdelivr.net"],
       "script-src":[ "'self'", "http://127.0.0.1:5000/bfa76213-edda-4b7c-ac9f-8e456ba8e500", "https://cdn.jsdelivr.net", "nonce"]}

# HTTP Strict Transport Security Header
# Tells browsers to connect via HTTPS
hsts = {"max-age": 31536000, "includeSubDomains": True} # Max age for 1 year

# Enforcing Security Headers
talisman.force_https = True
talisman.session_cookie_http_only = True
talisman.session_cookie_secure = True
talisman.x_xss_protection = True # X-XSS Protection
# talisman.x_content_type_options = True #Prevent MIME attacks
talisman.session_cookie_samesite = "Strict"
talisman.content_security_policy_nonce_in=["script-src"]

# Adding headers to talisman
talisman.content_security_policy = csp
talisman.strict_transport_security = hsts

# Initialising EventsLogger
log = EventLogger()
log.init_logger()

# ROUTES

# Creating a route decorator for home, which is a login section
@app.route('/', methods=["GET","POST"])
def index():
    # Checking if request is a post request
    if request.method == "POST":
        # Getting information from request
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Retrieved login details: {username}, {password}")
        # Using user authentication method to see if user exists
        result = User.authenticate(username, password)

        if result:
            print(f"Result: {result.create_key_pair()}")
            keypair =result.create_key_pair()
            # Creating key value pair for user object
            print(f"User: {keypair}")
            # Creating session variables for keeping track of logged in user
            session['user_id'] = keypair['id']
            session['username'] = keypair['username']
            session['role'] = keypair['role']
            flash("Successfully Logged-In")
            # Logging regestration
            log.log_login("Loggin", "User Successfully logged in", keypair['id'])
            # redirecting to home page
            return redirect('home')
        else:
            flash("Username does not exist")
            # Logging an attempt at login
            log.log_unsuccessful_login("Loggin", "User Failed to Log in", session["username"])
            return redirect('/')
    return render('login.html')

# Creating a route for registration
@app.route('/new', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirm_password")

        if password == confirmation:
            name_result = User.get_user_by_username(username)
            email_result = User.get_user_by_email(email)

            if (name_result is None) or (email_result is None):
                new_user = User(username, email, password)
                result = new_user.db_save()
                flash("Registration Successfull")
                user_id = User.get_user_by_username(username)
                if user_id:
                    # Making a log entry
                    log.log_registration("Registation", "User has Registered for the website", user_id)
                return redirect('/')
            else:
                flash("")
                flash("Unable to Register")
                return redirect('new')
    return render('register.html')

# Route for home page
# Page generated after successful login
@app.route('/home', methods=["GET", "POST"])
def home():
    # Obtain users blogs and disply them
    username = session['username']
    print(f'Username of session: {username}')
    blog_results = Blog.get_all_user_blogs(username)

    if blog_results is not None:
        print(f"First user blog found: {blog_results[0]}")

    # Creating local variables for tracking status
    user_search = False
    search_made = False
    search_blogs = []
    search_word = None

    # Perform user search
    if request.method == "POST":
        # Get searched word from form
        search_word = request.form.get('search')
        # Register search was performed
        search_made = True
        # Return searched blogs
        search_blogs = Blog.search(search_word)
        print(f"Found blog by search: {search_blogs}")

        # Register that user searched if blogs were found
        if search_blogs:
            user_search = True
            log.log_search("Searched for Blog", "Blog Found", session["user_id"])

        log.log_search("Searched for Blog", "Nothing Found", session["user_id"])
    # Render the details in home.html
    return render('home.html', blogs = blog_results, search_blogs = search_blogs, user_search = user_search, search_made = search_made, search_word = search_word)


# Route for creating a blog
@app.route('/create', methods=["GET", "POST"])
def create_blog():
    if request.method == "POST":
        blog_title = request.form.get('title')
        blog_content = request.form.get('content')

        if blog_title and blog_content:
            user_id = session['user_id']
            user_blog = Blog(user_id, blog_title, blog_content)
            blog_date = user_blog.created_at.date
            result = user_blog.db_save()
            if result:
                print('Created new blog')
                log.log_blog_creation("Blog Created", "New Blog has Been Created", user_id)
                return render('blog.html', blog = user_blog, blog_date = blog_date, session = session)
            else:
                flash("Unable to create the blog")
                log.log_blog_creation("Blog Not Created", "Attempt to Create a Blog has been Unsuccesful", user_id)
                return redirect('create')

    return render('create.html')

# Route for showing blog
@app.route('/blog/<int:blog_id>')
def blog(blog_id):

    returned_data = Blog.get_blog_by_id(blog_id)
    print(f"Blog returned: {returned_data}")
    blog = {}
    try:
        blog["id"] = blog_id
        blog['title'] = returned_data[0][0]
        blog['content'] = returned_data[0][2]
        blog['username'] = returned_data[0][1]
        blog["user_id"] = returned_data[0][3]
        log.log_blog_displayed("Blog Displayed", "Blog has been generated for User", session["user_id"])
    except Exception as e:
        print("Error occured creating Blog Page")
        log.log_blog_displayed("Blog Not Displayed", "Blog has not been generated", session["user_id"])
        return render('home.html')
    return render('blog.html', blog = blog, session = session)

# Route for Blog Deletion
@app.route('/delete_blog/<int:id>', methods=['POST'])
def delete_blog(id):

    if id:
        print(f"Blog ID: {id}")
        user_id = session['user_id']
        result = Blog.delete(id)
        if result:
            print('Blog deleted')
            log.log_blog_deleted("Blog Deleted", "Blog has been deleted", user_id)
        else:
            print('Blog not deleted')
            log.log_blog_deleted("Blog Not Deleted", "Blog has not been deleted", user_id)
    return redirect('/home')

# Method for logging out of a session
@app.route('/logout')
def logout():
    log.log_user_logged_out("User Logged Out", "User has successfully logged out", session["user_id"])
    # Clearing session
    session.clear()
    # Re-directing to login page
    return redirect('/')

# Making sure the app.py is automatically run when it is the main file.
if __name__ == "__main__":
    app.run()