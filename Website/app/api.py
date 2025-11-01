# https://stackoverflow.com/questions/21689364/method-not-allowed-flask-error-405 Fixed 405 error, didn't put GET in methods
# Professor Bowe helped us because we were unable to get things working with the template. Turns out we were accidentally creating a new instance lol!
# Template kept giving errors that were parameter related for the sql calls. Turns out you have to put a comma after even if there's nothing else so
# it is still recognized as a tuple thanks to the google AI when I looked up the error I was getting.
# I then had issues getting the template recognized and was checking the Flask tutorial we were provided and noticed he called his folder
# templates. I looked it up and according to the AI, you have to call the folder with your pages templates for the path to be recognized.
# Found this (https://www.geeksforgeeks.org/python/how-to-build-a-web-app-using-flask-and-sqlite-in-python/#) when trying to figure out why the animal 
# information was not printing. Found out everything is tuples. Tuples all the way down. This led to me getting the animal information outputted.
from flask import Flask, render_template
app = Flask(__name__)
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
    ('Happy Tails Shelter', 'info@happytails.org', '555-1111', '321 Shelter Ln', NULL, 'Springfield', 'IL', '62704', 1, '2025-01-15', 1, 50, 30, 1, 1)
    """)

    # Insert Animals
    cursor.execute("""
    INSERT INTO Animal (shelter_id, animal_id, name, type, breed, sex, foster, adopt, status, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered)
    VALUES
    (1, 1, 'Buddy', 'Dog', 'Labrador Retriever', 'Male', 1, 1, 'Available', '2025-02-05', 1, '2025-03-10', 1, 1),
    (1, 2, 'Misty', 'Cat', 'Siamese', 'Female', 0, 1, 'Adopted', '2025-01-22', 1, '2025-02-15', 1, 1),
    (1, 3, 'Rocky', 'Dog', 'German Shepherd', 'Male', 0, 0, 'In Shelter', '2025-03-01', 1, '2025-03-20', 1, 0)
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

# (COMPLETED) HOME - HOME - HOME - HOME - HOME - HOME - HOME - HOME - HOME - HOME #
#---------------------------------------------------------------------------------------------------#

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
@app.route("/index/animal/<int:animalID>", methods = ['GET', 'POST'])
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
