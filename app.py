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

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
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

SELF = '\'self\''

csp = {"default-src": SELF,
       "img-src": '*',
       "style-src": [ SELF, "https://cdn.jsdelivr.net"],
       "script-src":[ SELF, "http://127.0.0.1:5000/bfa76213-edda-4b7c-ac9f-8e456ba8e500", "https://cdn.jsdelivr.net", "nonce"]}

# HTTP Strict Transport Security Header
# Tells browsers to connect via HTTPS
hsts = {"max-age": 31536000, "includeSubDomains": True} # Max age for 1 year

# Enforcing Security Headers
talisman.force_https = True
talisman.session_cookie_http_only = True
talisman.session_cookie_secure = True
talisman.x_xss_protection = True # X-XSS Protection
# talisman.x_content_type_options = True #Prevent MIME attacks
talisman.session_cookie_samesite = "Lax"
talisman.content_security_policy_nonce_in=["script-src"]

# Adding headers to talisman
talisman.content_security_policy = csp
talisman.strict_transport_security = hsts

# Initialising EventsLogger
log = EventLogger.init_logger()

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
            # redirecting to home page
            return redirect('home')
        else:
            flash("Username does not exist")
            return redirect('/')
    return render('login.html')

# Creating a route decorator for registration
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
                new_user.db_save()
                flash("Registration Successfull")
                return redirect('/')
            else:
                flash("")
                flash("Unable to Register")
                return redirect('new')
    return render('register.html')

# VULNERABILITY: User input is reflected back without any checks or validation
# Reflected XSS
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

    # Render the details in home.html
    return render('home.html', blogs = blog_results, search_blogs = search_blogs, user_search = user_search, search_made = search_made, search_word = search_word)


# VULNERABILITY: XSS is stored on the database and can be retrieved
# Stored XSS
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
                return render('blog.html', blog = user_blog, blog_date = blog_date)
            else:
                flash("Unable to create the blog")
                return redirect('create')

    return render('create.html')

# To-Complete
@app.route('/blog/<int:blog_id>')
def blog(blog_id):

    returned_data = Blog.get_blog_by_id(blog_id)
    print(f"Blog returned: {returned_data}")
    blog = {}
    try:
        blog['title'] = returned_data[0][0]
        blog['content'] = returned_data[0][2]
        blog['username'] = returned_data[0][1]
    except Exception as e:
        print("Error occured creating Blog Page")
        return render('home.html')


    return render('blog.html', blog = blog)

#
@app.route('/delete_blog', methods=['POST'])
def delete_blog():
    id = request.form.get('blog_id')
    print(f"Blog ID: {id}")
    result = Blog.delete(id)
    if result:
        print('Blog deleted')
        return redirect('home')
    return None

# Method for logging out of a session
@app.route('/logout')
def logout():
    # Clearing session
    session.clear()
    # Re-directing to login page
    return redirect('/')

# Making sure the app.py is automatically run when it is the main file.
if __name__ == "__main__":
    app.run()