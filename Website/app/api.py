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
from flask import Flask, render_template
from . import app
import sqlite3

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
    ('Happy Tails Shelter', 'info@happytails.org', '555-1111', '321 Shelter Ln', NULL, 'Springfield', 'IL', '62704', 1, '2025-01-15', 1, 50, 30, 1, 1),
    ('Safe Paws Rescue', 'contact@safepaws.org', '555-2222', '89 Rescue Road', NULL, 'Madison', 'WI', '53703', 2, '2025-02-01', 1, 40, 25, 12, 8),
    ('Second Chance Animals', 'hello@secondchance.org', '555-3333', '14 Hope Ave', 'Suite B', 'Denver', 'CO', '80205', 3, '2025-03-12', 0, 60, 40, 30, 15),
    ('Furever Home Sanctuary', 'support@fureverhome.com', '555-4444', '700 Pawprint Dr', NULL, 'Austin', 'TX', '73301', 4, '2025-01-22', 1, 80, 50, 45, 25),
    ('Loving Hearts Animal Center', 'info@lovinghearts.net', '555-5555', '902 Kindness St', 'Building 2', 'Portland', 'OR', '97201', 5, '2025-04-05', 1, 35, 20, 18, 9),
    ('Paws & Whiskers Haven', 'support@pawswhiskers.org', '555-6666', '1200 Furry Rd', NULL, 'Atlanta', 'GA', '30301', 6, '2025-05-10', 0, 25, 18, 10, 6),
    ('Bright Horizons Animal Shelter', 'staff@brighthorizons.org', '555-7777', '55 Sunrise Ct', NULL, 'Seattle', 'WA', '98101', 7, '2025-03-30', 1, 70, 50, 48, 30),
    ('Rescue Ridge', 'info@rescueridge.org', '555-8888', '777 Ridge Lane', NULL, 'Phoenix', 'AZ', '85001', 8, '2025-02-18', 0, 45, 25, 20, 13)
    """)

    # Insert Animals
    cursor.execute("""
    INSERT INTO Animal (shelter_id, animal_id, name, type, breed, sex, foster, adopt, status, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered)
    VALUES
    (2, 4, 'Luna', 'Cat', 'Maine Coon', 'Female', 1, 0, 'Fostered', '2025-02-18', 1, '2025-03-22', 1, 1),
    (2, 5, 'Max', 'Dog', 'Golden Retriever', 'Male', 0, 1, 'Adopted', '2025-01-12', 1, '2025-02-01', 1, 1),
    (3, 6, 'Daisy', 'Dog', 'Beagle', 'Female', 1, 0, 'Fostered', '2025-02-25', 0, '2025-01-12', 1, 0),
    (3, 7, 'Shadow', 'Cat', 'Domestic Shorthair', 'Male', 0, 0, 'In Shelter', '2025-03-15', 1, '2025-03-28', 1, 1),
    (4, 8, 'Bella', 'Dog', 'Pit Bull Mix', 'Female', 0, 1, 'Adopted', '2025-01-30', 1, '2025-02-20', 1, 1),
    (4, 9, 'Oliver', 'Cat', 'Bengal', 'Male', 1, 0, 'Fostered', '2025-03-03', 1, '2025-03-25', 1, 0),
    (5, 10, 'Coco', 'Dog', 'Poodle', 'Female', 0, 0, 'In Shelter', '2025-02-01', 0, '2025-01-12', 1, 0),
    (5, 11, 'Milo', 'Cat', 'Tabby', 'Male', 0, 1, 'Adopted', '2025-01-15', 1, '2025-02-17', 1, 1),
    (6, 12, 'Zeus', 'Dog', 'Husky', 'Male', 1, 0, 'Fostered', '2025-03-11', 1, '2025-03-25', 1, 0),
    (6, 13, 'Willow', 'Cat', 'Persian', 'Female', 0, 0, 'In Shelter', '2025-02-26', 0,'2025-01-12', 0, 0)
    """)

    # # Insert Foster (Laura Kim fostering Buddy)
    # cursor.execute("""
    # INSERT INTO Foster (account_id, animal_id, shelter_id, other_pets, children, num_adults, notes, datetime_start, datetime_end)
    # VALUES
    # (3, 1, 1, 2, 1, 2, 'Very active foster family with fenced yard.', '2025-03-10', '2025-05-15'),
    # (4, 2, 1, 0, 0, 1, 'Single adult with quiet home. No other pets.', '2025-01-05', '2025-02-20'),
    # (5, 3, 2, 1, 1, 2, 'Family has small dog, good with cats.', '2025-04-01', '2025-04-30'),
    # (6, 1, 3, 3, 0, 2, 'Experienced foster home, multiple past fosters.', '2025-06-10', '2025-07-22'),
    # (7, 4, 2, 0, 2, 3, 'Home-school family, someone is always home.', '2025-02-15', '2025-03-29'),
    # (8, 5, 3, 2, 0, 1, 'Quiet retired foster, fenced yard and dog door.', '2025-03-01', '2025-04-15'),
    # (9, 6, 1, 0, 0, 1, 'First-time foster, small apartment.', '2025-05-20', '2025-06-10'),
    # (10, 2, 2, 1, 2, 2, 'Animal-loving household with teens, energetic dog.', '2025-01-20', '2025-03-05')
    # """)

    # # Insert Adoption (James Miller adopted Misty)
    # cursor.execute("""
    # INSERT INTO Adoption (account_id, animal_id, fee_amount, fee_payed)
    # VALUES
    # (2, 2, 100, 100),
    # (2, 1, 150, 150),
    # (2, 3, 50, 50),
    # (2, 2, 10, 10),
    # (2, 4, 100, 100),
    # (2, 6, 50, 50),
    # (2, 2, 60, 60)
    # """)

    # # Insert ShelterOwner (Emily Johnson owns the shelter)
    # cursor.execute("""
    # INSERT INTO ShelterOwner (shelter_id, account_id)
    # VALUES
    # (2,4),
    # (3,6),
    # (4,7),
    # (5,8)
    # """)

    conn.commit()

    conn.close()

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
@app.route("/home/<int:shelterID>", methods = ['GET'])
def main(shelterID = 0):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    shelter = []
    shelter = cursor.execute(('SELECT name, shelter_id FROM Shelter WHERE shelter_id = ?'), (shelterID,)).fetchone()
    animals = cursor.execute(('SELECT animal_id, name, type, breed, sex FROM Animal WHERE shelter_id = ?'), (shelterID,)).fetchall()
    conn.close()
    if not shelter:
        return "No shelter found."
    return render_template('home.html', animals = animals, shelter = shelter, indexLine = "/home/" + str(shelterID))



# (COMPLETED) SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL - SINGLE ANIMAL #
#---------------------------------------------------------------------------------------------------#
"""
Routes: /animal/int
Methods: GET
Template: animal.html
Returns: Returns the information for a single animal
"""
@app.route("/animal/<int:shelterID>/<int:animalID>", methods = ['GET'])
def index_by_id(shelterID = 1, animalID = 0):
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    animal = cursor.execute(('SELECT name, type, breed, animal_id, sex FROM Animal WHERE animal_id = ?'), (animalID,)).fetchone()
    conn.close()
    if not animal:
       return "Animal not found."
    return render_template("animal.html", animal=animal, indexLink = "/home/" + str(shelterID))


# (NOT COMPLETED) ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT #
#---------------------------------------------------------------------------------------------------#

#create a new account
@app.route("/login")
def login():
    return ("connects to account page based on id if username and pass match")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
