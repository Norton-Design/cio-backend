
# Run this app:

    1. clone repo
    2. install python3
    3. cd into project directory
    4. run "python3 -m venv venv"
    5. run "source venv/bin/activate"
    6. run "pip install -r requirements.txt"
    7. create .env file in root directory and set the path for the .data file: 
    '''
    DATA_PATH=<path_string_to_data_file>
    '''


    The following is what mine looked like:
    '''
    DATA_PATH="./datastore/data/messages.1.data"
    '''
    8. run "flask run"

# Thoughts:
    1. after generating data and parsing it, noticed that one of the events has "user_id". 
    Is this consistant with what we should expect with input, a mistake. I'll have to figure out later...
    2. Add event in data_store feels messy, need to refactor it later
    3. DataStore needs to be broken up into 3 classes: UserStore, EventStore, and DataStore
    4. I need to go back and remove access to the datastore attributes...
    5. I need to setup proper error handling back here...
    6. I have a strong desire to abstract out a User class for the routes, to get make things more consistant, and move away from the DataStore being so generic in it's naming. Would this just become redundant though....
    7. pagination is rough back here because of the deletion of users; this layer is usually abstracted away for reasons like this. For the sake of short term accuracy, I'll implement this like it'll be used directly with the frontend, and come back for the come up with a non-brute force approach. Man, I hope these ids are in order.
    8. Why would a customer create request already contain a user_id, that makes no sense at all. To be consistant, I have to keep it(?) but at no point should we need to return an available user_id up to the frontend just to pass it back again. 
    9. Man, it would be a terrible time to find out that Users and Customers are different in this project (they definitely are in the real thing, this project looks like an amalgamation).
    10. events key on new customer response? I'll do it, but feels unnecessary.

# Testing the Frontend and Backend together
    Bug #1: Forgot that JS timestamps are accurate to the millisecond, creating a problem hydra... 