# https://stackoverflow.com/questions/21689364/method-not-allowed-flask-error-405 Fixed 405 error, didn't put GET in methods
# Professor Bowe helped us because we were unable to get things working with the template. Turns out we were accidentally creating a new instance lol!
# Template kept giving errors that were parameter related for the sql calls. Turns out you have to put a comma after even if there's nothing else so
# it is still recognized as a tuple thanks to the google AI when I looked up the error I was getting.
# I then had issues getting the template recognized and was checking the Flask tutorial we were provided and noticed he called his folder
# templates. I looked it up and according to the AI, you have to call the folder with your pages templates for the path to be recognized.
# Found this (https://www.geeksforgeeks.org/python/how-to-build-a-web-app-using-flask-and-sqlite-in-python/#) when trying to figure out why the animal 
# information was not printing. Found out everything is tuples. Tuples all the way down. This led to me getting the animal information outputted.
from flask import Flask, render_template
from . import app
import sqlite3

DATABASE = 'animal_shelter.db'

@app.route("/<int:shelterID>", methods = ['GET', 'POST'])
@app.route("/index/<int:shelterID>", methods = ['GET', 'POST'])
def main(shelterID = 0):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
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
