import json

class DataStore:
    def __init__(self):
        self.events = {}
        self.users = {}
        self.create_datastore()

    def create_datastore(self):
        with open('./datastore/data/messages.1.data', 'r') as f:
            lines = f.readlines()
            for line in lines:
                parsed_line = json.loads(line)
                if parsed_line['type'] == 'event':
                    self.handle_event(parsed_line)
                elif parsed_line['type'] == 'attributes':
                    self.handle_attributes(parsed_line)
    
    def handle_event(self, event_message):
        pathological_inputs = []
        if 'user_id' not in event_message:
            # What to do with this edgecase??
            pathological_inputs.append(event_message)
        else:
            return self.add_event(event_message)

    def add_event(self, event_message):
        # This is an ugly function...
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
                

    def handle_attributes(self, attribute_message):
        user_id = int(attribute_message['user_id'])
        message_timestamp = attribute_message['timestamp']
        data = attribute_message['data']
        
        if user_id in self.users:
            # check data and modify
            curr_user = self.users[user_id]
            curr_timestamp = curr_user['last_updated']
            curr_attrs = curr_user['attributes']
            for key, value in data.items():
                if key in curr_attrs:
                    # check and update
                    potential_attr_pair = (value, message_timestamp)
                    curr_attrs[key] = self.most_recent_attribute(curr_attrs[key], potential_attr_pair)
                else:
                    curr_attrs[key] = (value, message_timestamp)
            if  message_timestamp > curr_timestamp:
                curr_user['last_updated'] = message_timestamp
        else: 
            parsed_data = {}
            for key, value in data.items():
                parsed_data[key] = (value, message_timestamp)
            new_user = {
                "id": user_id,
                "last_updated": message_timestamp,
                "attributes": parsed_data
            }
            self.users[user_id] = new_user

    def most_recent_attribute(self, curr_attr_pair, new_attr_pair):
        if curr_attr_pair[1] > new_attr_pair[1]:
            return curr_attr_pair
        else:
            return new_attr_pair

    def read_events_by_user_id(self, user_id):
        if user_id in self.events:
            formatted_user_events = {}
            user_events = self.events[user_id]
            for key in user_events.keys():
                formatted_user_events[key] = len(user_events[key])
            return formatted_user_events
        else:
            print('user_id not found in EVENTS, handle error here <-------')
            return None


    def read_users_by_user_id(self, user_id):
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
            user_events = self.read_events_by_user_id(user_id)
            if user_events:
                formatted_user['events'] = user_events
            return formatted_user
        else:
            print('user_id not found in USERS, handle error here <-------')
            return None






