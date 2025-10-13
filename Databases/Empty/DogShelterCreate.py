import sqlite3

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

conn.close()

