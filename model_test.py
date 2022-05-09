import sqlite3
import unittest
from model import BankDatabase
import sqlite3
class model_test(unittest.TestCase):

    ##only use this test with a non existing user - will not implement delete user 
    def test_new_registered_user(self):
        bank_database = BankDatabase()
        username = "" #use a different username here
        bank_database.register_new_user(username, "cake123")
        expectedValue = 100
        connection = sqlite3.connect("BambEuroBank.db")
        cursor = connection.cursor()
        user_balance = cursor.execute("SELECT COUNT(ID) FROM AccountHasBambEuro, Account, User WHERE AccountHasBambEuro.AccountID = Account.AccountID AND Account.UserID = User.UserID AND User.UserName = '" + username + "';").fetchall()[0][0]
        self.assertEquals(expectedValue, user_balance)

    def test_validate_user_exists(self):
        bank_database = BankDatabase()
        actual_value = bank_database.validate_user_exists("test_user01")
        expected_value = True
        self.assertEqual(expected_value,actual_value)
    
    def test_validate_login_credentials(self):
        bank_database = BankDatabase()
        actual_value = bank_database.validate_login_credentials("test_user01", "cake123")
        expected_value = True
        self.assertEqual(expected_value,actual_value)
        
    def test_retrieve_account_balance(self):
        bank_database = BankDatabase()
        actual_value = bank_database.retrieve_account_balance("test_user01")
        expected_value = 100
        self.assertEqual(expected_value,actual_value)
    
    def test_transfer_to_account(self):
        bank_database = BankDatabase()
        sender = "test_user01"
        recipient = "test_user02"
        bank_database.transfer_to_account(sender, recipient, 20)
        expectedValue = 80
        connection = sqlite3.connect("BambEuroBank.db")
        cursor = connection.cursor()
        user_balance = cursor.execute("SELECT COUNT(ID) FROM AccountHasBambEuro, Account, User WHERE AccountHasBambEuro.AccountID = Account.AccountID AND Account.UserID = User.UserID AND User.UserName = '" + sender + "';").fetchall()[0][0]
        cursor.close()
        self.assertEquals(expectedValue, user_balance)
        bank_database.transfer_to_account(recipient, sender, 20)
    
    def test_retrieve_transactions(self):
        bank_database = BankDatabase()
        transactions = bank_database.retrieve_transactions("test_user03")
        expected_value = 2
        actual_value = len(transactions)
        self.assertEqual(expected_value, actual_value)