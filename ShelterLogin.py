"""
render template - renders HTML template
request - gets data forms (login/register)
redirect, url_for - redirects users to routes

flask login - for logging in and out
UserMixin - allows the user class to handle authentification methods

werkzeug.security used for hashing and checking passwords

WILL STILL NEED: htmls for register, login, and userHomePage

"""

from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

#used by Flask to securely sign session cookies
app.config['SECRET_KEY'] = 'secret_key' # Replace with a strong, unique secret key

#manages login session
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #if a user tries to access a protected route, directs them to login

class User(UserMixin): #represents logged in user. UserMixin is used so Flask-Login can handle the authentification automatically
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    #looks up a user by id
    @staticmethod
    def get(user_id):
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            #returns user if found
            return User(user_data[0], user_data[1], user_data[2])
        return None

#loads the current user from the session
@login_manager.user_loader
def load_user(user_id):
    #connects the user id to the user
    return User.get(user_id)

#Routes

#registration; displays form in both GET and POST
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #generates hashed pw
        hashed_password = generate_password_hash(password)

        #inserts the new user into the database
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            #stops for duplicate username
            pass
        finally:
            conn.close()
    return render_template('register.html')

#for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #searches for user by the username
        conn = sqlite3.connect('login.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        #if username and password matches
        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user) #logs the user in
            return redirect(url_for('userHomePage'))
    return render_template('login.html')

@app.route('/logout')
@login_required #makes sure only logged in people can log out
def logout(): #logs out current user
    logout_user()
    return redirect(url_for('login'))

#logs the user into their home page
@app.route('/userHomePage')
@login_required
def dashboard():
    return f"Welcome, {current_user.username}!"

if __name__ == '__main__':
    # Initializes database
    conn = sqlite3.connect('login.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

    app.run(debug=True)