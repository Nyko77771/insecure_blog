from flask import Flask, render_template, request, session, redirect, flash
import os
from dotenv import load_dotenv
# Importing my models:
from models.user import User


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
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.authenticate(username, password)

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash("Successfully Logged-In")
            return redirect('home.html')
        else:
            flash("Username does not exist")
            redirect('login.html')
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
            user = User.db_save()

    return render('register.html')

# TO-DO!!!
# VULNERABILITY: User input is reflected back without any checks or validation
# Reflected XSS
@app.route('/home')
def home():
    session['username'] = 'Sophia'
    return render('home.html', user_search=None)

# TO-DO!!!
# VULNERABILITY: XSS is stored on the database and can be retrieved
# Stored XSS
@app.route('/create')
def create_blog():
    return render('create.html')

# To-Complete
@app.route('/blog')
def blog_page():
    return render('blog.html')



# TO-DO!!!
# VULNERABILITY: User name is reflected in the URL
# DOM based XSS
@app.route('/user/<name>')
def userPage(name):
    return "<h1>Hello {}</h1>".format(name)


if __name__ == "__main__":
    app.run()