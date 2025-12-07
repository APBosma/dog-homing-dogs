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
from . import app
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
        shelterPasscode INTEGER NOT NULL,
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
        shelter_id INTEGER,
        type TEXT NOT NULL CHECK(type IN ('shelter', 'owner')),
        FOREIGN KEY (shelter_id) REFERENCES Shelter(shelter_id)
    )
    """)

    conn.commit()

    # Insert Accounts (some are adopters, fosters, shelter staff)
    cursor.execute("""
    INSERT OR IGNORE INTO Account (type, firstname, lastname, email, phone, street1, datetime_created, datetime_modified)
    VALUES 
    ('staff', 'Emily', 'Johnson', 'emily.johnson@shelter.org', '555-1001', '123 Oak St', '2025-01-10', '2025-03-12'),
    ('adopter', 'James', 'Miller', 'james.miller@example.com', '555-2002', '45 Pine Ave', '2025-02-02', '2025-02-02'),
    ('foster', 'Laura', 'Kim', 'laura.kim@example.com', '555-3003', '78 Maple Rd', '2025-03-15', '2025-05-01'),
    ('adopter', 'Carlos', 'Hernandez', 'carlos.hernandez@example.com', '555-4004', '56 Elm St', '2025-03-20', '2025-03-20')
    """)

    # Insert Shelter
    cursor.execute("""
    INSERT OR IGNORE INTO Shelter (name, email, phone, street1, street2, city, state, zip, account_id, date_shelter_added, no_kill, max_dogs, max_cats, dogs, cats, shelterPasscode)
    VALUES
    ('Happy Tails Shelter', 'info@happytails.org', '555-1111', '321 Shelter Ln', NULL, 'Springfield', 'IL', '62704', 1, '2025-01-15', 1, 50, 30, 1, 1, 1234),
    ('Safe Paws Rescue', 'contact@safepaws.org', '555-2222', '89 Rescue Road', NULL, 'Madison', 'WI', '53703', 2, '2025-02-01', 1, 40, 25, 12, 8, 1234),
    ('Second Chance Animals', 'hello@secondchance.org', '555-3333', '14 Hope Ave', 'Suite B', 'Denver', 'CO', '80205', 3, '2025-03-12', 0, 60, 40, 30, 15, 1234),
    ('Furever Home Sanctuary', 'support@fureverhome.com', '555-4444', '700 Pawprint Dr', NULL, 'Austin', 'TX', '73301', 4, '2025-01-22', 1, 80, 50, 45, 25, 1234),
    ('Loving Hearts Animal Center', 'info@lovinghearts.net', '555-5555', '902 Kindness St', 'Building 2', 'Portland', 'OR', '97201', 5, '2025-04-05', 1, 35, 20, 18, 9, 1234),
    ('Paws & Whiskers Haven', 'support@pawswhiskers.org', '555-6666', '1200 Furry Rd', NULL, 'Atlanta', 'GA', '30301', 6, '2025-05-10', 0, 25, 18, 10, 6, 1234),
    ('Bright Horizons Animal Shelter', 'staff@brighthorizons.org', '555-7777', '55 Sunrise Ct', NULL, 'Seattle', 'WA', '98101', 7, '2025-03-30', 1, 70, 50, 48, 30, 1234),
    ('Rescue Ridge', 'info@rescueridge.org', '555-8888', '777 Ridge Lane', NULL, 'Phoenix', 'AZ', '85001', 8, '2025-02-18', 0, 45, 25, 20, 13, 1234)
    """)

    # Insert Animals
    cursor.execute("""
    INSERT OR IGNORE INTO Animal (shelter_id, animal_id, name, type, breed, sex, foster, adopt, status, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered)
    VALUES
    (1, 1, 'Buddy', 'Dog', 'Labrador Retriever', 'Male', 1, 1, 'Available', '2025-02-05', 1, '2025-03-10', 1, 1),
    (1, 2, 'Misty', 'Cat', 'Siamese', 'Female', 0, 1, 'Adopted', '2025-01-22', 1, '2025-02-15', 1, 1),
    (1, 3, 'Rocky', 'Dog', 'German Shepherd', 'Male', 0, 0, 'In Shelter', '2025-03-01', 1, '2025-03-20', 1, 0),
    (2, 4, 'Luna', 'Cat', 'Maine Coon', 'Female', 1, 0, 'Fostered', '2025-02-18', 1, '2025-03-22', 1, 1),
    (2, 5, 'Max', 'Dog', 'Golden Retriever', 'Male', 0, 1, 'Adopted', '2025-01-12', 1, '2025-02-01', 1, 1),
    (3, 6, 'Daisy', 'Dog', 'Beagle', 'Female', 1, 0, 'Fostered', '2025-02-25', 0, NULL, 1, 0),
    (3, 7, 'Shadow', 'Cat', 'Domestic Shorthair', 'Male', 0, 0, 'In Shelter', '2025-03-15', 1, '2025-03-28', 1, 1),
    (4, 8, 'Bella', 'Dog', 'Pit Bull Mix', 'Female', 0, 1, 'Adopted', '2025-01-30', 1, '2025-02-20', 1, 1),
    (4, 9, 'Oliver', 'Cat', 'Bengal', 'Male', 1, 0, 'Fostered', '2025-03-03', 1, '2025-03-25', 1, 0),
    (5, 10, 'Coco', 'Dog', 'Poodle', 'Female', 0, 0, 'In Shelter', '2025-02-01', 0, NULL, 1, 0),
    (5, 11, 'Milo', 'Cat', 'Tabby', 'Male', 0, 1, 'Adopted', '2025-01-15', 1, '2025-02-17', 1, 1),
    (6, 12, 'Zeus', 'Dog', 'Husky', 'Male', 1, 0, 'Fostered', '2025-03-11', 1, '2025-03-25', 1, 0),
    (6, 13, 'Willow', 'Cat', 'Persian', 'Female', 0, 0, 'In Shelter', '2025-02-26', 0, NULL, 0, 0)
    """)

    # Insert Foster (Laura Kim fostering Buddy)
    cursor.execute("""
    INSERT OR IGNORE INTO Foster (account_id, animal_id, shelter_id, other_pets, children, num_adults, notes, datetime_start, datetime_end)
    VALUES
    (3, 1, 1, 2, 1, 2, 'Very active foster family with fenced yard.', '2025-03-10', '2025-05-15'),
    (4, 2, 1, 0, 0, 1, 'Single adult with quiet home. No other pets.', '2025-01-05', '2025-02-20'),
    (5, 3, 2, 1, 1, 2, 'Family has small dog, good with cats.', '2025-04-01', '2025-04-30'),
    (6, 1, 3, 3, 0, 2, 'Experienced foster home, multiple past fosters.', '2025-06-10', '2025-07-22'),
    (7, 4, 2, 0, 2, 3, 'Home-school family, someone is always home.', '2025-02-15', '2025-03-29'),
    (8, 5, 3, 2, 0, 1, 'Quiet retired foster, fenced yard and dog door.', '2025-03-01', '2025-04-15'),
    (9, 6, 1, 0, 0, 1, 'First-time foster, small apartment.', '2025-05-20', '2025-06-10'),
    (10, 2, 2, 1, 2, 2, 'Animal-loving household with teens, energetic dog.', '2025-01-20', '2025-03-05')
    """)

    # Insert Adoption (James Miller adopted Misty)
    cursor.execute("""
    INSERT OR IGNORE INTO Adoption (account_id, animal_id, fee_amount, fee_payed)
    VALUES
    (2, 2, 100, 100),
    (2, 1, 150, 150),
    (2, 3, 50, 50),
    (2, 2, 10, 10),
    (2, 4, 100, 100),
    (2, 6, 50, 50),
    (2, 2, 60, 60)
    """)

    # Insert ShelterOwner (Emily Johnson owns the shelter)
    cursor.execute("""
    INSERT OR IGNORE INTO ShelterOwner (shelter_id, account_id)
    VALUES
    (1, 1),
    (2,4),
    (3,6),
    (4,7),
    (5,8)
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
Template: index.html
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
@app.route("/<int:shelterID>", methods = ['GET'])
@app.route("/home/<int:shelterID>", methods = ['GET'])
def main(shelterID = 0):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    shelter = cursor.execute(('SELECT name FROM Shelter WHERE shelter_id = ?'), (shelterID,)).fetchone()
    animals = cursor.execute(('SELECT animal_id, name, type, breed, sex FROM Animal WHERE shelter_id = ?'), (shelterID,)).fetchall()
    conn.close()
    if not shelter:
        return render_template('home.html', animals = animals, loggedIn = current_user.is_authenticated, shelterID = shelterID)
    
    return render_template('home.html', animals = animals, shelter = shelter, loggedIn = current_user.is_authenticated, shelterID = shelterID)



# (COMPLETED) SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL #
#---------------------------------------------------------------------------------------------------#
"""
Routes: /animal/int
Methods: GET
Template: animal.html
Returns: Returns the information for a single animal
"""
@app.route("/animal/<int:animalID>", methods = ['GET'])
def index_by_id(animalID = 0):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    animal = cursor.execute(('SELECT name, type, status, shelter_id, breed, animal_id, sex, date_time_arrived, vaccines, spayed_neutered FROM Animal WHERE animal_id = ?'), (animalID,)).fetchone()
    conn.close()
    if not animal:
       return "Animal not found."
    return render_template("animal.html", animal=animal)

   
# Add Animal - Add Animal - Add Animal - Add Animal - Add Animal - Add Animal - Add Animal - Add Animal #
#---------------------------------------------------------------------------------------------------#

@app.route("/addAnimal/<int:shelterID>", methods = ['GET', 'POST'])
@login_required
def addAnimal(shelterID = 0):
    if request.method == 'GET':
        return render_template("addAnimal.html", shelterID = shelterID)
    if request.method == 'POST':
        name = request.form.get('name')
        type_ = request.form.get('type')
        breed = request.form.get('breed')
        sex = request.form.get('sex')
        status = request.form.get('status') or None
        date_time_arrived = request.form.get('date_time_arrived') or None
        chipped = 1 if request.form.get('chipped') else 0
        date_last_vet_visit = request.form.get('date_last_vet_visit') or None
        vaccines = 1 if request.form.get('vaccines') else 0
        spayed_neutered = 1 if request.form.get('spayed_neutered') else 0

        # checkboxes – they only exist if checked
        foster = 1 if request.form.get('foster') else 0
        adopt = 1 if request.form.get('adopt') else 0

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Animal (name, type, breed, shelter_id, sex, foster, adopt, status, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, type_, breed, shelterID, sex, foster, adopt, status, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered))

        # after inserting, go back to the shelter page
    return redirect(f"/home/{shelterID}")

# button to link to adoption form, and shelter view

# Login and Registration - Login and Registration - Login and Registration - Login and Registration #
#---------------------------------------------------------------------------------------------------#

#registration; displays form in both GET and POST
@app.route('/signup.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        shelter_choice = request.form['shelterChoice']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        street = request.form['street']

        #makes sure everything is properly filled out in sign up
        required_user_fields = [username, password, firstname, lastname, email, phone, street]
        if any(field.strip() == "" for field in required_user_fields):
            return render_template("signup.html", error="Please fill out all information.")

        #extra information to fill out if "shelterOwner" is selected
        if shelter_choice == "shelterOwner":
            required_shelter_fields = {
                "Shelter Name": request.form.get("newShelterName", ""),
                "Shelter Email": request.form.get("shelterEmail", ""),
                "Shelter Phone": request.form.get("shelterPhone", ""),
                "Street Address 1": request.form.get("street1", ""),
                "City": request.form.get("city", ""),
                "State": request.form.get("state", ""),
                "ZIP Code": request.form.get("zip", ""),
                "No Kill": request.form.get("no_kill", ""),
                "Max Dogs": request.form.get("max_dogs", ""),
                "Max Cats": request.form.get("max_cats", ""),
                "Accepting Dogs": request.form.get("dogs", ""),
                "Accepting Cats": request.form.get("cats", ""),
                "Shelter Passcode": request.form.get("shelterPasscode", "")
            }

            missing = [label for label, value in required_shelter_fields.items() if value == ""]

            if missing:
                return render_template(
                    "signup.html",
                    error="Missing Shelter Owner Fields: " + ", ".join(missing)
                )

        # Determine user type and shelter association
        if shelter_choice == "shelterOwner":
            type = "owner"
            #inserting into shelter table
            newShelterName = request.form['newShelterName']
            shelterEmail = request.form['shelterEmail']
            shelterPhone = request.form['shelterPhone']
            street1 = request.form['street1']
            street2 = request.form.get('street2')
            city = request.form['city']
            state = request.form['state']
            zip_code = request.form['zip']
            no_kill = request.form['no_kill']
            max_dogs = request.form['max_dogs']
            max_cats = request.form['max_cats']
            dogs = request.form['dogs']
            cats = request.form['cats']
            shelterPasscode = request.form['shelterPasscode']

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Shelter (
                    name, email, phone, street1, street2,
                    city, state, zip,
                    date_shelter_added,
                    no_kill, max_dogs, max_cats, dogs, cats,
                    shelterPasscode
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, DATE('now'), ?, ?, ?, ?, ?, ?)
            """, (
                newShelterName,
                shelterEmail,
                shelterPhone,
                street1,
                street2,
                city,
                state,
                zip_code,
                no_kill,
                max_dogs,
                max_cats,
                dogs,
                cats,
                shelterPasscode
            ))

            #automatically sets lastrowid to the PK of the shelter row
            shelter_id = cursor.lastrowid

            conn.commit()
            conn.close()
    
        else:
            type = "shelter"
            account_type = "shelter"
            shelter_id = int(shelter_choice)
        account_type = "shelter"
        
        #generates hashed pw
        hashed_password = generate_password_hash(password)

        #inserts the new user into the database
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO login (username, password, type, shelter_id) VALUES (?, ?, ?, ?)", (username, hashed_password, account_type, shelter_id))
            cursor.execute("INSERT INTO Account (type, firstname, lastname, email, phone, street1, datetime_created) VALUES (?, ?, ?, ?, ?, ?, DATE('now'))", (type, firstname, lastname, email, phone, street))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            #stops for duplicate username
            return "Username Already Exists"
        finally:
            conn.close()
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    shelters = cursor.execute('SELECT name, shelter_id FROM Shelter').fetchall()
    return render_template('signup.html', shelters = shelters)

#for login
@app.route('/login.html', methods=['GET', 'POST'])
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
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT shelter_id FROM login WHERE id = ?", (user.id,))
            row = cursor.fetchone()
            conn.close()

            user_shelter_id = row[0]

            if user.type == 'shelter' and user_shelter_id:
                return redirect(url_for('shelter_dashboard'))

            elif user.type == 'owner':
                return redirect(url_for('owner_dashboard'))

            else:
                return "Shelter user has no shelter ID"
            
        else:
            return "Invalid Username or Password"
    
    return render_template('login.html')

@app.route('/logout')
@login_required #makes sure only logged in people can log out
def logout(): #logs out current user
    logout_user()
    return redirect(url_for('login'))

#for our different account types. 
#logs user into shelter
@app.route('/shelter_dashboard')
@login_required
def shelter_dashboard():
    if current_user.type != 'shelter':
        return "Access Denied", 403

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT shelter_id FROM login WHERE id = ?", (current_user.id,))
    row = cursor.fetchone()
    conn.close()

    if row and row['shelter_id']:
        return redirect(url_for('main', shelterID=row['shelter_id']))

    return "Error: No shelter associated with this account"

#logs user into owner
@app.route('/owner_dashboard')
@login_required
def owner_dashboard():
    if current_user.type != 'owner':
        return "Access Denied: Only owners can view this page.", 403

    # Redirect shelter owners to the main index page
    return redirect(url_for('index'))


if __name__ == '__main__':
    preset() #creates our db and adds our info 
    app.run(debug=True)
