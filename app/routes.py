from app import app
from datastore import DataStore

@app.route("/")
def hello_world():
    return "hello, world"

# Remove after testing...
# store = DataStore()
# print(store.read_events_by_user_id(1))
# print(store.events[1])
# print(store.read_users_by_user_id(1))