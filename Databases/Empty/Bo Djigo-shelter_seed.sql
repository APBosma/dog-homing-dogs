
PRAGMA foreign_keys = ON;


DROP TABLE IF EXISTS Shelter_Owners;
DROP TABLE IF EXISTS Adoption;
DROP TABLE IF EXISTS Fosters;
DROP TABLE IF EXISTS Animal;
DROP TABLE IF EXISTS Account;
DROP TABLE IF EXISTS Shelter;


CREATE TABLE Shelter (
  id                INTEGER PRIMARY KEY,
  name              TEXT NOT NULL,
  email             TEXT,
  phone_number      TEXT,
  street1           TEXT,
  street2           TEXT,
  city              TEXT,
  state             TEXT,
  zipcode           TEXT,
  date_shelter_added DATE,
  no_kill_shelter   INTEGER DEFAULT 0, 
  max_dogs          INTEGER,
  max_cats          INTEGER,
  cats              INTEGER DEFAULT 1,
  dogs              INTEGER DEFAULT 1  
);

CREATE TABLE Account (
  account_id   INTEGER PRIMARY KEY,
  account_type TEXT NOT NULL, 
  name         TEXT NOT NULL,
  email        TEXT,
  phone_number TEXT,
  street1      TEXT,
  street2      TEXT,
  city         TEXT,
  state        TEXT,
  zipcode      TEXT
);

CREATE TABLE Animal (
  animal_id            INTEGER PRIMARY KEY,
  shelter_id           INTEGER NOT NULL REFERENCES Shelter(id) ON DELETE CASCADE,
  animal_type          TEXT NOT NULL, 
  sex                  TEXT CHECK (sex IN ('Male','Female','Unknown')),
  status               TEXT, 
  available_foster     INTEGER DEFAULT 0,
  available_adopt      INTEGER DEFAULT 1,
  date_time_arrived    TEXT, 
  chipped              INTEGER DEFAULT 0,
  date_last_vet_visit  TEXT,
  vaccines             INTEGER DEFAULT 0,
  spayed_neutered      INTEGER DEFAULT 0
);

CREATE TABLE Fosters (
  foster_id        INTEGER PRIMARY KEY,
  account_id       INTEGER NOT NULL REFERENCES Account(account_id) ON DELETE CASCADE,
  animal_id        INTEGER NOT NULL REFERENCES Animal(animal_id) ON DELETE CASCADE,
  shelter_id       INTEGER NOT NULL REFERENCES Shelter(id) ON DELETE CASCADE,
  other_pets       INTEGER DEFAULT 0,
  children         INTEGER DEFAULT 0,
  number_of_adults INTEGER DEFAULT 1,
  notes            TEXT,
  date_time_start  TEXT,
  date_time_end    TEXT
);

CREATE TABLE Adoption (
  adoption_id   INTEGER PRIMARY KEY,
  account_id    INTEGER NOT NULL REFERENCES Account(account_id) ON DELETE CASCADE,
  animal_id     INTEGER NOT NULL REFERENCES Animal(animal_id) ON DELETE CASCADE,
  fee_amount    REAL,
  fee_payed     INTEGER DEFAULT 0,
  date_adopted  TEXT,
  date_returned TEXT
);

CREATE TABLE Shelter_Owners (
  shelter_id INTEGER NOT NULL REFERENCES Shelter(id) ON DELETE CASCADE,
  owner_id   INTEGER NOT NULL REFERENCES Account(account_id) ON DELETE CASCADE,
  PRIMARY KEY (shelter_id, owner_id)
);

-- Shelters
INSERT INTO Shelter (id, name, email, phone_number, street1, city, state, zipcode, date_shelter_added, no_kill_shelter, max_dogs, max_cats, cats, dogs) VALUES
(1, 'Happy Tails Shelter', 'contact@happytails.org', '512-555-0110', '123 Paw St', 'Austin', 'TX', '73301', '2024-01-15', 1, 40, 30, 1, 1),
(2, 'Whisker Haven', 'hello@whiskerhaven.org', '415-555-0142', '88 Meow Ave', 'San Francisco', 'CA', '94102', '2024-03-02', 1, 10, 50, 1, 0),
(3, 'Four Paws Rescue', 'team@fourpaws.net', '206-555-0188', '740 Bark Blvd', 'Seattle', 'WA', '98101', '2023-11-20', 0, 35, 20, 1, 1);

-- Accounts (adopters/fosters/owners/staff)
INSERT INTO Account (account_id, account_type, name, email, phone_number, street1, city, state, zipcode) VALUES
(1, 'Owner',  'Avery Chen',     'avery@happytails.org', '512-555-1000', '1 Shelter Way', 'Austin', 'TX', '73301'),
(2, 'Owner',  'Jordan Patel',   'jordan@whiskerhaven.org', '415-555-2000', '88 Meow Ave', 'San Francisco', 'CA', '94102'),
(3, 'Owner',  'Sam Rivera',     'sam@fourpaws.net',     '206-555-3000', '740 Bark Blvd', 'Seattle', 'WA', '98101'),
(4, 'Both',   'Mia Thompson',   'mia.t@example.com',    '512-555-1111', '12 Oak Dr', 'Austin', 'TX', '73301'),
(5, 'Foster', 'Diego Alvarez',  'diego.a@example.com',  '415-555-2222', '914 Pine St', 'San Francisco', 'CA', '94103'),
(6, 'Adopter','Priya Singh',    'priya.s@example.com',  '206-555-3333', '401 5th Ave', 'Seattle', 'WA', '98104'),
(7, 'Both',   'Chris Johnson',  'chris.j@example.com',  '512-555-4444', '93 Maple Rd', 'Austin', 'TX', '73301'),
(8, 'Foster', 'Lila Grant',     'lila.g@example.com',   '415-555-5555', '512 Mission St', 'San Francisco', 'CA', '94105'),
(9, 'Adopter','Noah Kim',       'noah.k@example.com',   '206-555-6666', '221B Cedar Ln', 'Seattle', 'WA', '98109');

-- Link shelter owners
INSERT INTO Shelter_Owners (shelter_id, owner_id) VALUES
(1,1),(2,2),(3,3);

-- Animals
INSERT INTO Animal (animal_id, shelter_id, animal_type, sex, status, available_foster, available_adopt, date_time_arrived, chipped, date_last_vet_visit, vaccines, spayed_neutered) VALUES
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
(112,2,'Dog','Male','Available',1,1,'2024-03-10T09:40:00',0,'2024-03-18',0,0);

-- Foster placements
INSERT INTO Fosters (foster_id, account_id, animal_id, shelter_id, other_pets, children, number_of_adults, notes, date_time_start, date_time_end) VALUES
(1,4,103,1,1,0,2,'Experienced with senior dogs','2024-02-20T18:00:00',NULL),
(2,5,107,2,0,1,1,'Quiet apartment; cat tree available','2024-03-03T10:00:00',NULL),
(3,8,106,2,1,0,1,'Works from home','2024-03-05T09:00:00',NULL),
(4,7,104,1,1,2,2,'Short-term medical hold','2024-03-15T12:00:00','2024-03-22T12:00:00'),
(5,4,109,3,0,0,2,'Good yard space','2024-02-25T14:30:00',NULL);

-- Adoptions
INSERT INTO Adoption (adoption_id, account_id, animal_id, fee_amount, fee_payed, date_adopted, date_returned) VALUES
(1,6,111,125.00,1,'2024-01-20',NULL),
(2,9,108,200.00,1,'2024-02-10',NULL),
(3,4,105,90.00,1,'2024-03-12',NULL),
(4,7,110,110.00,1,'2024-03-18',NULL);
