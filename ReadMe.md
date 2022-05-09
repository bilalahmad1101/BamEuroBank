# BambEuroBank 

## Plan

- Use MVC pattern
- Use SQLite local database - would usually use AWS ec2 and mysql server
    Following Tables will be created:
        - User
        - Account
        - BambEuro
        - AccountHasBambEuro (link table of account and BambEuro)
        - Transaction
        
- 3 interfaces (html web pages with basic design) - login - sign up - account
- create unit tests for model (database interaction) and view(selenium tests)
- controller will utilise the Flask Framework and I will use Python

## assumptions 
- features are:
    - log in
    - create a new user
    - view user balance
    - view all transactions of the user logged in
    - Transfer money to another user
- Security wont be considered (seems outside the scope of this task):
    e.g. 
    - storing credentials in plain text
    - hardcoding credentials in tests
    - holding a user session whilst logged in



