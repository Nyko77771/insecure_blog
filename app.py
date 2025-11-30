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
            return redirect('login')
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
                user = User.db_save()
                flash("Registration Successfull")
                redirect('login.html')
            else:
                flash("")
                flash("Unable to Register")
                redirect('register.html')
    return render('register.html')

# VULNERABILITY: User input is reflected back without any checks or validation
# Reflected XSS
@app.route('/home', methods=["GET", "POST"])
def home():
    # Obtain users blogs and disply them
    username = session['username']
    print(f'Username of session: {username}')
    blog_results = Blog.get_all_user_blogs(username)

    user_search = False
    search_made = False
    search_blogs = []

    if request.method == "POST":
        search_word = request.form.get('search')
        search_made = True
        print(f"Search made: {search_made}")
        search_blogs = Blog.search(search_word)
        print(f"Blog searches: {search_blogs} ")

        if search_blogs:
            user_search = True

    return render('home.html', blogs = blog_results, search_blogs = search_blogs, user_search = user_search, search_made = search_made)


# TO-DO!!!
# VULNERABILITY: XSS is stored on the database and can be retrieved
# Stored XSS
@app.route('/create')
def create_blog():
    return render('create.html')

# To-Complete
@app.route('/blog')
def blog_page():
    session['user_id'] = 1
    session['role'] = 'admin'
    return render('blog.html', blog_id = 1, )

@app.route('/delete_blog', methods=['POST'])
def delete_blog():
    id = request.form.get('blog_id')
    print(f"Blog ID: {id}")
    return None

# TO-DO!!!
# VULNERABILITY: User name is reflected in the URL
# DOM based XSS
@app.route('/user/<name>')
def userPage(name):
    return "<h1>Hello {}</h1>".format(name)


# Method for logging out of a session
@app.route('/logout')
def logout():
    # Clearing session
    session.clear()

    # Re-directing to login page
    return redirect('/')





if __name__ == "__main__":
    app.run()