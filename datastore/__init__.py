import json

class DataStore:
    def __init__(self):
        self.events = {}
        self.users = {}
        self.create_datastore()

    def create_datastore(self):
        with open('./data/messages.1.data', 'r') as f:
            lines = f.readlines()
            for line in lines:
                parsed_line = json.loads(line)
                if parsed_line['type'] == 'event':
                    self.handle_event(parsed_line)
                elif parsed_line['type'] == 'attributes':
                    self.handle_attributes(parsed_line)
    
    def handle_event(self, event_message):
        # print(event_message)
        pathological_inputs = []
        if 'user_id' not in event_message:
            # What to do with this edgecase??
            pathological_inputs.append(event_message)
        else:
            return self.add_event(event_message)

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
                

    def handle_attributes(self, attribute_message):
        user_id = int(attribute_message['user_id'])
        message_timestamp = attribute_message['timestamp']
        data = attribute_message['data']
        
        if user_id in self.users:
            # check data and modify
            new_user = self.users[user_id]
            current_customer_timestamp = new_user['last_updated']
            if  message_timestamp > current_customer_timestamp:
                new_user['last_updated'] = message_timestamp
                new_user['attributes'] = data
        else: 
            # add new user and parse data
            new_user = {
                "id": user_id,
                "last_updated": message_timestamp,
                "attributes": data
            }
            self.users[user_id] = new_user


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
            for key in datastore_user.keys():
                formatted_user[key] = datastore_user[key]
            user_events = self.read_events_by_user_id(user_id)
            if user_events:
                formatted_user['events'] = user_events
            return formatted_user
        else:
            print('user_id not found in USERS, handle error here <-------')
            return None


# Remove after testing...
store = DataStore()
# print(store.read_events_by_user_id(1))
# print(store.events[1])
print(store.read_users_by_user_id(1))




