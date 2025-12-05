# importing flask methods
from flask import Flask, render_template, request, session, redirect, flash
# Imporing dotenv library for accessing dotenv variables
from dotenv import load_dotenv
# Importing my models:
from models.user import User
from models.blogs import Blog


# Creating flask instance
app = Flask(__name__)
render = render_template
# VULNERABILITY: Hard Coded Secret Key
app.secret_key = "BAD_SECRET"
# Setting up a debugging enviroment
app.config["DEBUG"] = True

# ROUTES

# Creating a route decorator for home, which is a login section
@app.route('/', methods=["GET","POST"])
def index():
    # Checking if request is a post request
    if request.method == "POST":
        # Getting information from request
        username = request.form.get('username')
        password = request.form.get('password')

        # Using user authentication method to see if user exists
        user = User.authenticate(username, password)

        if user:
            # Creating key value pair for user object
            keypair = user.create_key_pair()
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
        blog["blog_id"] = blog_id
    except Exception as e:
        print("Error occured creating Blog Page")
        return render('home.html')


    return render('blog.html', blog = blog)

#
@app.route('/delete_blog/<int:blog_id>', methods=['POST'])
def delete_blog(blog_id):
    print(f"Blog ID: {blog_id}")
    result = Blog.delete(blog_id)
    if result:
        print('Blog deleted')
    return redirect('/home')

# TO-DO!!!
# VULNERABILITY: User name is reflected in the URL
# DOM based XSS

# Method for logging out of a session
@app.route('/logout')
def logout():
    # Clearing session
    session.clear()
    # Re-directing to login page
    return redirect('/')


if __name__ == "__main__":
    app.run()