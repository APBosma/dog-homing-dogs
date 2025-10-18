from flask import Flask
import sqlite3
import os

currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

DATABASE = os.path.join(currentdirectory, "animal_shelter.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    return conn

@app.route("/")
def main():
    return ("Homepage")

#create a new account
@app.route("/login")
def login():
    return ("connects to account page based on id if username and pass match")

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

if __name__ == "__main__":
    app.run()