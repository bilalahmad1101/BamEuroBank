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

## How to run and set project up
    Prereqs:
        - python
        - pip
        - Flask
        - venv
        - selenium
        
    Instructions:
        1. create a virtual environment in the project in which you can use pip to install flask and selenium
        2. activate the virtual environment with "source env/bin/activate"
        3. Run the application with "python app.py"
        4. In a browser, type "localhost:5000"
        5. this should bring up the log in page.
        
    Unit test instructions (with VScode):
        1. Open project in vscode
        2. Click on the testing button from the left menu (The last icon shaped like a flask)
        3. Select configure tests.
        4. select unit tests
        5. select root directory
        6. select "_test.py"
        7. both model tests and selenium tests will be available to run individually.
        NOTE: Ensure to use new user names for registering new users as deleting was not implemented ( both model and selenium test)
        NOTE: Ensure that the app.py controller is running when runnning selenium tests.
## Other comments

    - Usually when creating features I follow this structure: Create the function in model and test, create the route in controller, create the interface and test. Due to time constraints I impemented the entire model first, then the controller and then the interfaces.
    



