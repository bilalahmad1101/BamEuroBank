from flask import Flask, redirect, render_template, url_for, request
from sqlalchemy import false, true
import sys
from model import BankDatabase


app = Flask(__name__)


@app.route('/') #routes to homepage - login
def index():
    return render_template('index.html', login_failed=False)

@app.route('/login/', methods=['POST']) #carries out log in request
def login():
    if request.method == 'POST':
        username = request.form['login_username']
        password = request.form['login_password']
        bank_database = BankDatabase()
        if bank_database.validate_login_credentials(username,password): 
            return redirect(url_for('account',username = username)) #redirects to account page after successful login
        else:
            return render_template('index.html', login_failed=True) #reloads homepage due to failed login
        

@app.route('/sign-up/')
def sign_up():
    return render_template('sign_up.html', status="") #loads sign up page

@app.route('/create-account/', methods=['POST'])#carries out request to create a new account
def create_account():
    if request.method == 'POST':
        username = request.form['sign_up_username']
        password = request.form['sign_up_password']
        confirm_password = request.form['sign_up_confirm_password']
        if len(username) < 1 or len(password) < 1 or len(confirm_password) < 1:
            return render_template('sign_up.html', status="Please fill in all fields.") #reloads sign up page as fields were blank
        bank_database = BankDatabase()
        if password == confirm_password: 
            if not bank_database.validate_user_exists(username):
                bank_database.register_new_user(username,password)
                return redirect('/') #creates new account and redirects back to login page
            else:
                return render_template('sign_up.html', status="This user already exists. Try another username.") #reloads sign up page as user already exists
        else:
            return render_template('sign_up.html', status="Passwords do not match.") #reloads sign up page as password was not confirmed

        
@app.route('/account') #loads the users account page
def account():
    username = request.args['username'] #retrieves username from previous rerote
    bank_database = BankDatabase()
    balance = bank_database.retrieve_account_balance(username)
    transactions = bank_database.retrieve_transactions(username)
    return render_template('account.html', balance=balance, transactions=transactions, username=username)#loads the account page with users details

@app.route('/transfer/', methods=['POST'])#carries out request to transfer BambEuros to another user
def transfer():
    if request.method == 'POST':
        sender = request.form['username']
        recipient = request.form['send_to_text']
        amount = int(request.form['amount_text'])
        bank_database = BankDatabase()
        sender_balance = bank_database.retrieve_account_balance(sender)
        if bank_database.validate_user_exists(recipient):
            if  sender_balance > int(amount):
                bank_database.transfer_to_account(sender,recipient,amount)
                transactions = bank_database.retrieve_transactions(sender)
                sender_balance = bank_database.retrieve_account_balance(sender)
                return render_template('account.html', balance = sender_balance, transactions=transactions, username=sender, status="Transfer Complete") #carries out transfer and reloads page with updated details
            else:
                transactions = bank_database.retrieve_transactions(sender)
                return render_template('account.html', balance = sender_balance, transactions=transactions, username=sender, status="Insuficient funds")# reloads page as the user does not have enough bamberuos
        else:
            transactions = bank_database.retrieve_transactions(sender)
            return render_template('account.html', balance = sender_balance, transactions=transactions, username=sender, status="The user you are transfering to, does not exist")#reloads page as the recipient does not exist

if __name__ == "__main__":
    app.run(debug=True)