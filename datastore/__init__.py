import json
import time
import os
from datetime import datetime

DATA_PATH = os.getenv('DATA_PATH')

class DataStore:
    def __init__(self):
        self.events = {}
        self.users = {}
        self.user_total = 0
        self.next_available_user_id = 1
        self.create_datastore()
        self.set_next_available_user_id()

    def create_datastore(self):
        with open(DATA_PATH, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parsed_line = json.loads(line)
                if parsed_line['type'] == 'event':
                    self.screen_pathological_events(parsed_line)
                elif parsed_line['type'] == 'attributes':
                    self.update_user_attributes(parsed_line)
    
    def screen_pathological_events(self, event_message):
        if 'user_id' in event_message:
            self.add_event(event_message)

    def add_event(self, event_message):
        user_id = int(event_message['user_id'])
        event_id = event_message['id']
        event_name = event_message['name']

        if user_id in self.events:
            user_events = self.events[user_id]
            if event_name in user_events:
                event_set = user_events[event_name]
                if event_id not in event_set:
                    event_set.add(event_id)
            else:
                user_events[event_name] = set()
                user_events[event_name].add(event_id)
        else:
            event_set = set()
            event_set.add(event_id)
            self.events[user_id] = {}
            self.events[user_id][event_name] = event_set

    def update_user_attributes(self, user_data):
        user_id = int(user_data['user_id'])
        message_timestamp = int(user_data['timestamp'])
        data = user_data['data']
        
        if user_id in self.users:
            # check data and modify
            curr_user = self.users[user_id]
            curr_timestamp = curr_user['last_updated']
            curr_attrs = curr_user['attributes']
            for key, value in data.items():
                if key in curr_attrs and value == "**DELETE_ATTRIBUTE**":
                    del curr_attrs[key]
                elif key in curr_attrs:
                    # check and update
                    potential_attr_pair = (value, message_timestamp)
                    curr_attrs[key] = self.most_recent_attribute(curr_attrs[key], potential_attr_pair)
                else:
                    curr_attrs[key] = (value, message_timestamp)
            if  message_timestamp > curr_timestamp:
                curr_user['last_updated'] = message_timestamp
            return self.find_user_by_id(user_id)
        else: 
            self.create_user(data, user_id, message_timestamp)

    def most_recent_attribute(self, curr_attr_pair, new_attr_pair):
        if curr_attr_pair[1] > new_attr_pair[1]:
            return curr_attr_pair
        else:
            return new_attr_pair

    def find_events_by_user_id(self, user_id):
        if user_id in self.events:
            formatted_user_events = {}
            user_events = self.events[user_id]
            for key in user_events.keys():
                formatted_user_events[key] = len(user_events[key])
            return formatted_user_events
        else:
            return {}

    def find_user_by_id(self, user_id):
        if user_id in self.users:
            formatted_user = {}
            datastore_user = self.users[user_id]
            for key, value in datastore_user.items():
                if key == 'attributes':
                    parsed_attrs = {}
                    attrs = datastore_user['attributes']
                    for attr_key in attrs:
                        parsed_attrs[attr_key] = attrs[attr_key][0]
                    formatted_user['attributes'] = parsed_attrs                    
                else:
                    formatted_user[key] = value
            user_events = self.find_events_by_user_id(user_id)
            formatted_user['events'] = user_events
            return formatted_user
        else:
            return None

    def set_next_available_user_id(self):
        count = self.next_available_user_id
        while count in self.users:
            count += 1
        self.next_available_user_id = count

    def delete_user_by_id(self, user_id):
        user = self.users.pop(user_id, None)
        events = self.events.pop(user_id, None)
        self.user_total -= 1
        return user or events 

    def create_user(self, user_data, user_id=None, timestamp=None):
        if not user_id:
            user_id = self.next_available_user_id
        if not timestamp:
            timestamp = int(time.time())
        parsed_data = {}
        for key, value in user_data.items():
            parsed_data[key] = (value, timestamp)
        new_user = {
            "id": user_id,
            "last_updated": timestamp,
            "attributes": parsed_data
        }
        self.users[user_id] = new_user
        self.user_total += 1
        return self.users[user_id]


    def get_user_total(self):
        return self.user_total

    def paginated_collection(self, page, per_page):
        starting_id = (page - 1) * per_page + 1
        ending_id = page * per_page
        user_collection = []
        for n in range(starting_id, ending_id + 1):
            user = self.find_user_by_id(n)
            if user:
                user_collection.append(user)
        return user_collection





