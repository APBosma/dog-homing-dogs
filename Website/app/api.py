# https://stackoverflow.com/questions/21689364/method-not-allowed-flask-error-405 Fixed 405 error, didn't put GET in methods
# Professor Bowe helped us because we were unable to get things working with the template. Turns out we were accidentally creating a new instance lol!
# Template kept giving errors that were parameter related for the sql calls. Turns out you have to put a comma after even if there's nothing else so
# it is still recognized as a tuple thanks to the google AI when I looked up the error I was getting.
# I then had issues getting the template recognized and was checking the Flask tutorial we were provided and noticed he called his folder
# templates. I looked it up and according to the AI, you have to call the folder with your pages templates for the path to be recognized.
# Found this (https://www.geeksforgeeks.org/python/how-to-build-a-web-app-using-flask-and-sqlite-in-python/#) when trying to figure out why the animal 
# information was not printing. Found out everything is tuples. Tuples all the way down. This led to me getting the animal information outputted.
# I had seen previous mentions of a form with HTML so I looked up "HTML form" and used W3 for my form syntax since they're my go-to for
# documentation. This was used for login and sign up.

"""
Citations for login and registration:
I looked up methods to log into accounts using Flask and it gave me flask_login and the imports I used, what they do, and how to use them.
When I did this, it also gave me the werkzeug.security too, so I implimented it as well.
I looked up what UserMixin does and how to implement it.
With the registration and login routes, I knew how to organize them, but I did have to look up small issues I had like the the request methods.
I also looked at previously made portions of the API and implemented some of the calls that way.
"""


from flask import Flask, request, redirect, url_for, render_template
#from . import app
app = Flask(__name__)
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

#used by Flask to securely sign session cookies
app.config['SECRET_KEY'] = 'secret_key' #replace with secret key

#manages login session
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #if a user tries to access a protected route, directs them to login

DATABASE = 'animal_shelter.db'

def preset():
    conn = sqlite3.connect("animal_shelter.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Account (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL,
        firstname TEXT NOT NULL,
        lastname TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        street1 TEXT NOT NULL,
        datetime_created TEXT,
        datetime_modified TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Shelter (
        shelter_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        street1 TEXT NOT NULL,
        street2 TEXT,
        city TEXT NOT NULL,
        state TEXT NOT NULL,
        zip TEXT NOT NULL,
        account_id INTEGER,
        date_shelter_added TEXT,
        no_kill BOOLEAN NOT NULL,
        max_dogs INTEGER NOT NULL,
        max_cats INTEGER NOT NULL,
        dogs BOOLEAN NOT NULL,
        cats BOOLEAN NOT NULL,
        FOREIGN KEY (account_id) REFERENCES Account(account_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Animal (
        animal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        shelter_id INTEGER,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        breed TEXT NOT NULL,
        sex TEXT NOT NULL,
        foster INTEGER NOT NULL,
        adopt INTEGER NOT NULL,
        status TEXT NOT NULL,
        date_time_arrived TEXT NOT NULL,
        chipped BOOLEAN NOT NULL,
        date_last_vet_visit TEXT NOT NULL,
        vaccines BOOLEAN NOT NULL,
        spayed_neutered BOOLEAN NOT NULL,
        FOREIGN KEY (shelter_id) REFERENCES Shelter(shelter_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Foster (
        account_id INTEGER,
        animal_id INTEGER,
        shelter_id INTEGER NOT NULL,
        other_pets INTEGER NOT NULL,
        children INTEGER NOT NULL,
        num_adults INTEGER NOT NULL,
        notes TEXT,
        datetime_start TEXT NOT NULL,
        datetime_end TEXT NOT NULL,
        PRIMARY KEY (account_id, animal_id),
        FOREIGN KEY (account_id) REFERENCES Account(account_id),
        FOREIGN KEY (animal_id) REFERENCES Animal(animal_id),
        FOREIGN KEY (shelter_id) REFERENCES Shelter(shelter_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Adoption (
        account_id INTEGER NOT NULL,
        animal_id INTEGER NOT NULL,
        fee_amount INTEGER NOT NULL,
        fee_payed INTEGER NOT NULL,
        PRIMARY KEY (account_id, animal_id),
        FOREIGN KEY (account_id) REFERENCES Account(account_id),
        FOREIGN KEY (animal_id) REFERENCES Animal(animal_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ShelterOwner (
        shelter_id INTEGER,
        account_id INTEGER,
        PRIMARY KEY (shelter_id, account_id),
        FOREIGN KEY (shelter_id) REFERENCES Shelter(shelter_id),
        FOREIGN KEY (account_id) REFERENCES Account(account_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        type TEXT NOT NULL CHECK(type IN ('shelter', 'owner'))
    )
    """)

    conn.commit()

    # Insert Accounts (some are adopters, fosters, shelter staff)
    cursor.execute("""
    INSERT INTO Account (type, firstname, lastname, email, phone, street1, datetime_created, datetime_modified)
    VALUES 
    ('staff', 'Emily', 'Johnson', 'emily.johnson@shelter.org', '555-1001', '123 Oak St', '2025-01-10', '2025-03-12'),
    ('adopter', 'James', 'Miller', 'james.miller@example.com', '555-2002', '45 Pine Ave', '2025-02-02', '2025-02-02'),
    ('foster', 'Laura', 'Kim', 'laura.kim@example.com', '555-3003', '78 Maple Rd', '2025-03-15', '2025-05-01'),
    ('adopter', 'Carlos', 'Hernandez', 'carlos.hernandez@example.com', '555-4004', '56 Elm St', '2025-03-20', '2025-03-20')
    """)

    # Insert Shelter
    cursor.execute("""
    INSERT INTO Shelter (name, email, phone, street1, street2, city, state, zip, account_id, date_shelter_added, no_kill, max_dogs, max_cats, dogs, cats)
    VALUES
    ('Happy Tails Shelter', 'info@happytails.org', '555-1111', '321 Shelter Ln', NULL, 'Springfield', 'IL', '62704', 1, '2025-01-15', 1, 50, 30, 1, 1)
    """)

    # Insert Animals
    cursor.execute("""
    INSERT INTO Animal (shelter_id, animal_id, name, type, breed, sex, foster, adopt, status, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered)
    VALUES
    (1, 1, 'Buddy', 'Dog', 'Labrador Retriever', 'Male', 1, 1, 'Available', '2025-02-05', 1, '2025-03-10', 1, 1),
    (1, 2, 'Misty', 'Cat', 'Siamese', 'Female', 0, 1, 'Adopted', '2025-01-22', 1, '2025-02-15', 1, 1),
    (1, 7, 'Rocky', 'Dog', 'German Shepherd', 'Male', 0, 0, 'In Shelter', '2025-03-01', 1, '2025-03-20', 1, 0)
    """)

    # Insert Foster (Laura Kim fostering Buddy)
    cursor.execute("""
    INSERT INTO Foster (account_id, animal_id, shelter_id, other_pets, children, num_adults, notes, datetime_start, datetime_end)
    VALUES
    (3, 1, 1, 2, 1, 2, 'Very active foster family with fenced yard.', '2025-03-10', '2025-05-15')
    """)

    # Insert Adoption (James Miller adopted Misty)
    cursor.execute("""
    INSERT INTO Adoption (account_id, animal_id, fee_amount, fee_payed)
    VALUES
    (2, 2, 100, 100)
    """)

    # Insert ShelterOwner (Emily Johnson owns the shelter)
    cursor.execute("""
    INSERT INTO ShelterOwner (shelter_id, account_id)
    VALUES
    (1, 1)
    """)

    conn.commit()

    conn.close()

class User(UserMixin): #represents logged in user. UserMixin is used so Flask-Login can handle the authentification automatically
    def __init__(self, id, username, password, type):
        self.id = id
        self.username = username
        self.password = password
        self.type = type

    #looks up a user by id
    @staticmethod
    def get(user_id):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, type FROM login WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            #returns user if found
            return User(user_data[0], user_data[1], user_data[2], user_data[3])
        return None

#loads the current user from the session
@login_manager.user_loader
def load_user(user_id):
    #connects the user id to the user
    return User.get(user_id)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# (COMPLETED) INDEX #
#---------------------------------------------------------------------------------------------------#
"""
Routes: /, /index
Methods: GET
Template: index..html
Returns: Lists all shelters with their address, clicking the shelter takes you to the shelter's home page
"""
@app.route("/")
@app.route("/index")
def index():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    shelters = cursor.execute('SELECT name, shelter_id, street1, street2, city, state, zip FROM Shelter').fetchall()
    return render_template('index.html', shelters = shelters)

# (COMPLETED) HOME - HOME - HOME - HOME - HOME - HOME - HOME - HOME - HOME - HOME #
#---------------------------------------------------------------------------------------------------#
"""
Routes: /home/int
Methods: GET
Template: home.html
Returns: List of all animals at a shelter
"""
@app.route("/<int:shelterID>", methods = ['GET', 'POST'])
@app.route("/index/<int:shelterID>", methods = ['GET', 'POST'])
def main(shelterID = 0):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    shelter = []
    shelter = cursor.execute(('SELECT name FROM Shelter WHERE shelter_id = ?'), (shelterID,)).fetchone()
    animals = cursor.execute(('SELECT animal_id, name, type, breed, sex FROM Animal WHERE shelter_id = ?'), (shelterID,)).fetchall()
    conn.close()
    if not shelter:
        return render_template('index.html', animals = animals)
    
    return render_template('index.html', animals = animals, shelter = shelter)



# (COMPLETED) SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL #
#---------------------------------------------------------------------------------------------------#
"""
Routes: /animal/int
Methods: GET
Template: animal.html
Returns: Returns the information for a single animal
"""
@app.route("/animal/<int:animalID>", methods = ['GET', 'POST'])
def index_by_id(animalID = 0):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    animal = cursor.execute(('SELECT name, type, breed, animal_id, sex FROM Animal WHERE animal_id = ?'), (animalID,)).fetchone()
    conn.close()
    if not animal:
       return "Animal not found."
    return render_template("animal.html", animal=animal)


# (NOT COMPLETED) ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT #
#---------------------------------------------------------------------------------------------------#

#edit account
@app.route("/account/<int:account_id>/edit", methods = ["POST"])
def account_edit():
    return ("function to edit database info")
    
#view your account
@app.route("/account/<int:account_id>", methods = ["GET"])
def get_account(account_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM account WHERE account_id = ?", (account_id,))
    account = cursor.fetchone()
    conn.close()
    if account is None:
        return "Account not found"
    return str(account) #we can change this, its just so we can view for testing easier 

# show animal mini bio - if foster, we can have them be able to create and edit pet accounts, if they are with a shelter, same thing. can only manipulate the pets they added and removed (shelters must have approved users to manipulate thier database)
    
# Add Animal - Add Animal - Add Animal - Add Animal - Add Animal - Add Animal - Add Animal - Add Animal #
#---------------------------------------------------------------------------------------------------#

@app.route("/index/animal/<int:animal_id>/edit", methods = ["GET"])
def animal_edit():
    return ("function to edit animal info")

# button to link to adoption form, and shelter view

# Login and Registration - Login and Registration - Login and Registration - Login and Registration #
#---------------------------------------------------------------------------------------------------#

#registration; displays form in both GET and POST
@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #account_type = request.form['type']  # "shelter" or "owner" - didn't work with sign up page so I made a defined version for now
        account_type = "shelter"
        #generates hashed pw
        hashed_password = generate_password_hash(password)

        #inserts the new user into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO login (username, password, type) VALUES (?, ?, ?)", (username, hashed_password, account_type))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            #stops for duplicate username
            return "Username Already Exists"
        finally:
            conn.close()
    return render_template('signup.html')

#for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        #searches for user by the username
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, type FROM login WHERE username = ?", (username,))
        user_data = cursor.fetchone()
        conn.close()

        #if username and password matches
        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1], user_data[2], user_data[3])
            login_user(user) #logs the user in
            if user.type == 'shelter':
                return redirect(url_for('shelter_dashboard'))
            else:
                return redirect(url_for('owner_dashboard'))
            
        else:
            return "Invalid Username or Password"
    
    return render_template('login.html')

@app.route('/logout')
@login_required #makes sure only logged in people can log out
def logout(): #logs out current user
    logout_user()
    return redirect(url_for('login'))

#logs the user into their home page. will change when we work on different account types
@app.route('/userHomePage')
@login_required
def userHomePage():
    return f"Welcome, {current_user.username}!"

#for our different account types. 
#logs user into shelter
@app.route('/shelter_dashboard')
@login_required
def shelter_dashboard():
    if current_user.type != 'shelter':
        return "Access Denied: Only shelters can view this page.", 403
    return f"Welcome, shelter user {current_user.username}!"

#logs user into owner
@app.route('/owner_dashboard')
@login_required
def owner_dashboard():
    if current_user.type != 'owner':
        return "Access Denied: Only owners can view this page.", 403
    return f"Welcome, owner user {current_user.username}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
