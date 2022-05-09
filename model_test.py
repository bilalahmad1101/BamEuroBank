import sqlite3
import unittest
from model import BankDatabase
import sqlite3
class model_test(unittest.TestCase):

    ##only use this test with a non existing user - will not implement delete user 
    def test_new_registered_user(self):
        bank_database = BankDatabase()
        username = "test_user01"
        bank_database.register_new_user(username, "cake123")
        expectedValue = 100
        connection = sqlite3.connect("BambEuroBank.db")
        cursor = connection.cursor()
        user_balance = cursor.execute("SELECT COUNT(ID) FROM AccountHasBambEuro, Account, User WHERE AccountHasBambEuro.AccountID = Account.AccountID AND Account.UserID = User.UserID AND User.UserName = '" + username + "';").fetchall()[0][0]
        self.assertEquals(expectedValue, user_balance)