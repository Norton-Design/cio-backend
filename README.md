
Run this app:

    1. clone repo
    2. install python3
    3. cd into project directory
    4. run "python3 -m venv venv"
    5. run "source venv/bin/activate"
    6. run "pip install -r requirements.txt"
    7. adjust the path to the messages.data as needed <--- Check this later
    8. run "flask run"

Thoughts:
    1. after generating data and parsing it, noticed that one of the events has "user_id". 
    Is this consistant with what we should expect with input, a mistake. I'll have to figure out later...
    2. Add event in data_store feels messy, need to refactor it later
    3. DataStore needs to be broken up into 3 classes: UserStore, EventStore, and DataStore
    4. I need to go back and remove access to the datastore attributes...
    5. I need to setup proper error handling back here...