from flask import Flask, render_template

# Creating flask instance
app = Flask(__name__)
ren = render_template

# Creating a route decorator for home
@app.route('/')
def index():
    return ren('login.html')

@app.route('/new')
def register():
    return ren('register.html')

@app.route('/user/<name>')
def userPage(name):
    return "<h1>Hello {}</h1>".format(name)


if __name__ == "__main__":
    app.run()