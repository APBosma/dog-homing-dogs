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

# Inserts start here

cursor.execute(
    """
    -- Shelters
INSERT INTO Shelter (shelter_id, name, email, phone, street1, city, state, zip, date_shelter_added, no_kill, max_dogs, max_cats, cats, dogs) VALUES
(1, 'Happy Tails Shelter', 'contact@happytails.org', '512-555-0110', '123 Paw St', 'Austin', 'TX', '73301', '2024-01-15', 1, 40, 30, 1, 1),
(2, 'Whisker Haven', 'hello@whiskerhaven.org', '415-555-0142', '88 Meow Ave', 'San Francisco', 'CA', '94102', '2024-03-02', 1, 10, 50, 1, 0),
(3, 'Four Paws Rescue', 'team@fourpaws.net', '206-555-0188', '740 Bark Blvd', 'Seattle', 'WA', '98101', '2023-11-20', 0, 35, 20, 1, 1);""")

cursor.execute(
    """
-- Accounts (adopters/fosters/owners/staff)
INSERT INTO Account (account_id, type, firstname, lastname, email, phone, street1) VALUES
(1, 'Owner',  'Avery', 'Chen',     'avery@happytails.org', '512-555-1000', '1 Shelter Way'),
(2, 'Owner',  'Jordan', 'Patel',   'jordan@whiskerhaven.org', '415-555-2000', '88 Meow Ave'),
(3, 'Owner',  'Sam', 'Rivera',     'sam@fourpaws.net',     '206-555-3000', '740 Bark Blvd'),
(4, 'Both',   'Mia', 'Thompson',   'mia.t@example.com',    '512-555-1111', '12 Oak Dr'),
(5, 'Foster', 'Diego', 'Alvarez',  'diego.a@example.com',  '415-555-2222', '914 Pine St'),
(6, 'Adopter','Priya', 'Singh',    'priya.s@example.com',  '206-555-3333', '401 5th Ave'),
(7, 'Both',   'Chris', 'Johnson',  'chris.j@example.com',  '512-555-4444', '93 Maple Rd'),
(8, 'Foster', 'Lila', 'Grant',     'lila.g@example.com',   '415-555-5555', '512 Mission St'),
(9, 'Adopter','Noah', 'Kim',       'noah.k@example.com',   '206-555-6666', '221B Cedar Ln');""")

cursor.execute(
    """
-- Link shelter owners
INSERT INTO ShelterOwner (shelter_id, account_id) VALUES
(1,1),(2,2),(3,3);""")

cursor.execute(
    """
-- Animals
INSERT INTO Animal (animal_id, shelter_id, type, sex, status, available_foster, available_adopt, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered) VALUES
(101,1,'Dog','Male','Available',1,1,'2024-02-10T10:30:00',1,'2024-03-12',1,1),
(102,1,'Cat','Female','Available',0,1,'2024-02-18T14:00:00',1,'2024-03-05',1,1),
(103,1,'Dog','Female','Fostered',0,0,'2024-01-29T09:00:00',0,'2024-02-15',1,0),
(104,1,'Dog','Male','Hold',0,0,'2024-03-08T11:45:00',1,'2024-03-20',0,0),
(105,2,'Cat','Male','Available',1,1,'2024-03-01T13:20:00',1,'2024-03-10',1,1),
(106,2,'Cat','Female','Available',1,1,'2024-03-02T16:05:00',0,'2024-03-12',1,0),
(107,2,'Cat','Female','Fostered',0,0,'2024-02-20T08:10:00',1,'2024-03-01',1,1),
(108,3,'Dog','Male','Available',1,1,'2023-12-15T15:30:00',1,'2024-01-20',1,1),
(109,3,'Dog','Female','Available',1,1,'2024-01-10T12:00:00',0,'2024-02-05',1,0),
(110,3,'Cat','Male','Available',1,1,'2024-02-05T17:25:00',1,'2024-03-07',1,1),
(111,1,'Cat','Female','Adopted',0,0,'2023-12-28T10:00:00',1,'2024-01-15',1,1),
(112,2,'Dog','Male','Available',1,1,'2024-03-10T09:40:00',0,'2024-03-18',0,0);""")

cursor.execute(
    """
-- Foster placements
INSERT INTO Fosters (foster_id, account_id, animal_id, shelter_id, other_pets, children, number_of_adults, notes, date_time_start, date_time_end) VALUES
(1,4,103,1,1,0,2,'Experienced with senior dogs','2024-02-20T18:00:00',NULL),
(2,5,107,2,0,1,1,'Quiet apartment; cat tree available','2024-03-03T10:00:00',NULL),
(3,8,106,2,1,0,1,'Works from home','2024-03-05T09:00:00',NULL),
(4,7,104,1,1,2,2,'Short-term medical hold','2024-03-15T12:00:00','2024-03-22T12:00:00'),
(5,4,109,3,0,0,2,'Good yard space','2024-02-25T14:30:00',NULL);""")

cursor.execute(
    """
-- Adoptions
INSERT INTO Adoption (adoption_id, account_id, animal_id, fee_amount, fee_payed, date_adopted, date_returned) VALUES
(1,6,111,125.00,1,'2024-01-20',NULL),
(2,9,108,200.00,1,'2024-02-10',NULL),
(3,4,105,90.00,1,'2024-03-12',NULL),
(4,7,110,110.00,1,'2024-03-18',NULL);""")

conn.commit()

conn.close()

