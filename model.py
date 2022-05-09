import sqlite3
from tracemalloc import start
from importlib_metadata import NullFinder
from datetime import datetime
from sqlalchemy import false, null

class BankDatabase():
    
    def __init__(self):
        self.cursor = None

    def start_connection(self):
        connection = sqlite3.connect('BambEuroBank.db')
        self.cursor = connection
    
    def register_new_user(self, username, password):
        self.start_connection()
        #inserts new user details in the user table
        self.cursor.execute("INSERT INTO User(UserName,UserPassword) VALUES ('" 
        + username + "', '" + password + "');")
        self.cursor.commit()
        #retrieves user ID of the new record added to the user table
        UserID = str(self.cursor.execute("SELECT UserID FROM User WHERE UserName = '" 
        + username + "' AND UserPassword = '" + password + "';").fetchall()[0][0])
        self.cursor.commit()
        #inserts a new record in the account table for the new user
        self.cursor.execute("INSERT INTO Account(UserID, Balance) VALUES ('" 
        + UserID + "', '100');")
        self.cursor.commit()
        AccountID = str(self.cursor.execute("SELECT AccountID FROM Account WHERE UserID = '" 
        + UserID  + "';").fetchall()[0][0])
        self.cursor.commit()
        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #Gives user 100 BambEuros
        for i in range(0,100):
            #Inserts new BambEuro in BambEuro Table with Timestamp
            self.cursor.execute("INSERT INTO BambEuro(DepositDate) VALUES ('" 
            + date_and_time + "');")
            self.cursor.commit()
            #Retrieves the ID of the of the newly added BambEuro
            BambEuroID = str(self.cursor.execute("SELECT BambEuroID FROM BambEuro ORDER BY BambEuroID DESC LIMIT 1;").fetchall()[0][0])
            self.cursor.commit()
            #Assigns the new BambEuro to an account by adding a record to the link table
            self.cursor.execute("INSERT INTO AccountHasBambEuro(AccountID,BambEuroID) VALUES ('" 
            + AccountID + "', '" + BambEuroID + "');")
            self.cursor.commit()
        self.cursor.close()

    def validate_user_exists(self, username):
        self.start_connection()
        #retrieves username if it exists
        pulled_username = self.cursor.execute("SELECT UserName FROM User WHERE UserName ='" + username + "';").fetchall()
        self.cursor.commit()
        self.cursor.close()
        #returns true if the results are not empty
        if len(pulled_username) > 0:
            return True
        return False
    
    def validate_login_credentials(self, username, password):
        self.start_connection()
        #retrieves creds if record exists of given combination
        pulled_creds = self.cursor.execute("SELECT UserName, UserPassword FROM User WHERE UserName ='" + username + "' AND UserPassword = '" + password + "';").fetchall()
        self.cursor.commit()
        self.cursor.close()
        #returns true if the results are not empty
        if len(pulled_creds) > 0:
            return True
        return False
    
    def retrieve_account_balance(self, username):
        self.start_connection()
        #Quries account for balance for given username
        pulled_balance = self.cursor.execute("SELECT Balance FROM Account, User WHERE Account.UserID = User.UserID AND UserName ='" + username + "';").fetchall()[0][0]
        self.cursor.commit()
        self.cursor.close()
        return pulled_balance