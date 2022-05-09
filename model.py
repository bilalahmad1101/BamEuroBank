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
    
    def transfer_to_account(self, sender_username, recipient_username, transfer_amount):
        self.start_connection()
        #retieves Account details for both sender and recipient 
        sender_account = self.cursor.execute("SELECT AccountID, Balance FROM Account, User WHERE Account.UserID = User.UserID AND UserName ='" + sender_username + "';").fetchall()
        self.cursor.commit()
        recipient_account = self.cursor.execute("SELECT AccountID, Balance FROM Account, User WHERE Account.UserID = User.UserID AND UserName ='" + recipient_username + "';").fetchall()
        self.cursor.commit()
        date_and_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        #new record added for this Transaction
        self.cursor.execute("INSERT INTO 'Transaction'(SenderID, RecipientID, Date, Amount) VALUES ('" + str(sender_account[0][0]) + "', '" + str(recipient_account[0][0]) + "', '" + date_and_time + "', " + str(transfer_amount) + ");")
        self.cursor.commit()
        #The link table is updated to replace the senders account ID with the recipients account ID. The update is applied to the same amount of records as the transfer amount.
        self.cursor.execute("UPDATE AccountHasBambEuro SET AccountID = '" + str(recipient_account[0][0]) + "' WHERE rowid IN (SELECT rowid FROM AccountHasBambEuro WHERE AccountID ='" + str(sender_account[0][0]) + "' LIMIT " + str(transfer_amount) + ");" )
        self.cursor.commit()
        #The balance is updated for the sender and recipient based on the this transfer.
        self.cursor.execute("UPDATE Account SET Balance = " + str(sender_account[0][1] - transfer_amount) + " WHERE AccountID = '" + str(sender_account[0][0]) + "';")
        self.cursor.commit()
        self.cursor.execute("UPDATE Account SET Balance = " + str(recipient_account[0][1] + transfer_amount) + " WHERE AccountID = '" + str(recipient_account[0][0]) + "';")
        self.cursor.commit()
        self.cursor.close()
    
    def retrieve_transactions(self, username):
        self.start_connection()
        #Retrieves all transactions for given username - uses multiple select queries to retrieve names of sender and recipient
        transactions = self.cursor.execute("SELECT (SELECT UserName FROM User, Account WHERE 'Transaction'.SenderID = Account.AccountID AND Account.UserID = User.UserID) as Sender, (SELECT UserName FROM User, Account WHERE 'Transaction'.RecipientID = Account.AccountID AND Account.UserID = User.UserID) as Recipient, Amount, Date FROM 'Transaction', Account, User WHERE ('Transaction'.SenderID = Account.AccountID OR 'Transaction'.RecipientID = Account.AccountID) AND Account.UserID = User.UserID AND User.UserName = '" + username + "'  ORDER BY TransactionID DESC;").fetchall()
        self.cursor.commit()
        self.cursor.close()
        return transactions