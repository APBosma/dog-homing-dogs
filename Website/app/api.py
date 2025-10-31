# https://stackoverflow.com/questions/21689364/method-not-allowed-flask-error-405 Fixed 405 error, didn't put GET in methods
# Professor Bowe helped us because we were unable to get things working with the template. Turns out we were accidentally creating a new instance lol!
# Template kept giving errors that were parameter related for the sql calls. Turns out you have to put a comma after even if there's nothing else so
# it is still recognized as a tuple thanks to the google AI when I looked up the error I was getting.
# I then had issues getting the template recognized and was checking the Flask tutorial we were provided and noticed he called his folder
# templates. I looked it up and according to the AI, you have to call the folder with your pages templates for the path to be recognized.
from flask import Flask, render_template
from . import app
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(currentdirectory, "animal_shelter.db")

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

    # Inserts start here

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
    INSERT INTO Animal (shelter_id, name, type, breed, sex, foster, adopt, status, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered)
    VALUES
    (1, 'Buddy', 'Dog', 'Labrador Retriever', 'Male', 1, 1, 'Available', '2025-02-05', 1, '2025-03-10', 1, 1),
    (1, 'Misty', 'Cat', 'Siamese', 'Female', 0, 1, 'Adopted', '2025-01-22', 1, '2025-02-15', 1, 1),
    (1, 'Rocky', 'Dog', 'German Shepherd', 'Male', 0, 0, 'In Shelter', '2025-03-01', 1, '2025-03-20', 1, 0)
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



def get_db_connection():
    conn = sqlite3.connect('animal_shelter.db')
    return conn

@app.route("/<int:shelterID>", methods = ['GET', 'POST'])
@app.route("/index/<int:shelterID>", methods = ['GET', 'POST'])
def main(shelterID = 0):
    conn = get_db_connection()
    cursor = conn.cursor()
    everything = cursor.execute(('SELECT name, type, breed, sex FROM Animal WHERE shelter_id = ?'), (shelterID,)).fetchall()

    for row in everything:
        print(row)

    shelterName = cursor.execute(('SELECT name FROM Shelter WHERE shelter_id = ?'), (shelterID,)).fetchone()
    animals = cursor.execute(('SELECT name, type, breed, sex FROM Animal WHERE shelter_id = ?'), (shelterID,)).fetchall()
    conn.close()
    return render_template('index.html', animals = animals, shelterName = shelterName[0])

# ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT - ACCOUNT #
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
    
# Animal - Animal - Animal - Animal - Animal - Animal - Animal - Animal - Animal - Animal - Animal #
#---------------------------------------------------------------------------------------------------#

#main view - shows list of animals mini bio - sortable
@app.route("/view")
def animal_view():
    return ("entire database of animals, sortable by location/distance")
    
#detailed animal info
@app.route("/animal/<int:animal_id>")
def animal_info():
    return ("shows detailed animal information")

@app.route("/animal/<int:animal_id>/edit", methods = ["GET"])
def animal_edit():
    return ("function to edit animal info")

# button to link to adoption form, and shelter view

# if __name__ == "__main__":
#     print("at the bottom of api.py")
#     app.run()
