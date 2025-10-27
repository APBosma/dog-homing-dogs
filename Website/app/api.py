from flask import Flask, render_template
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

DATABASE = os.path.join(currentdirectory, "animal_shelter.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

#@app.route("/") #houses login button to take you to /login, and also shows the list of animals mini profile, which you can click to view more 
# https://stackoverflow.com/questions/21689364/method-not-allowed-flask-error-405 Fixed 405 error, didn't put GET in methods
@app.route("/<int:shelterID>")
@app.route("/index/<int:shelterID>", methods = ['GET', 'POST'])
def main(shelterID):
    conn = get_db_connection()
    shelterName = conn.execute(('SELECT name FROM Shelter WHERE shelter_id = ?'), shelterID).fetchone()
    animals = conn.execute(('SELECT * FROM Animal WHERE shelter_id = ?'), shelterID).fetchall()
    conn.close()
    return render_template('index.html', animals = animals, shelterName = str(shelterName))

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




if __name__ == "__main__":

    app.run()
