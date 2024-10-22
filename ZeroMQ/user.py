import zmq
import uuid
import threading
import json

class User:
    def __init__(self, name, message_server_address):
        self.name = name
        self.uuid = str(uuid.uuid4())
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(message_server_address)

    def get_group_list(self):
        self.socket.send_json({"request_type": "get_group_list"})
        response = self.socket.recv()
        
        groups_dict = json.loads(response.decode('utf-8'))
        print(f"{self.name} - Available Groups:")
        for group_name, group_address in groups_dict.items():
            print(group_name , " : " , group_address)
        
    def create_group(self, group_name):
        self.socket.send_json({"request_type": "create_group" , "group_name" : group_name})
        response = self.socket.recv_string()
        print(response)

    def join_group(self, group_name):
        self.socket.send_json({"request_type": "join_group", "group_name": group_name, "user_uuid": self.uuid})
        response = self.socket.recv_string()
        print(response)

    def leave_group(self, group_name):
        leave_request = {"request_type": "leave_group", "user_uuid": self.uuid, "group_name": group_name}
        self.socket.send_json(leave_request)
        response = self.socket.recv_string()
        print(response)

    def send_message(self, group_name, message):
        self.socket.send_json({"request_type": "send_message", "group_name": group_name, "user_uuid": self.uuid, "message_content": message})
        response = self.socket.recv_string()
        print(response)

    def get_messages(self, group_name, timestamp=None):
        
        self.socket.send_json({"request_type": "get_messages", "group_name": group_name, "user_uuid": self.uuid , "timestamp" : timestamp})
        # messages = self.socket.recv_json()
        try:
            messages = self.socket.recv_json()
            print(f"Messages from {group_name}:")
            for msg in messages:
                print(f"Timestamp: {msg['timestamp']}, User: {msg['user_uuid']}, Content: {msg['content']}")

        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON response: {messages}")
            print(f"Error details: {e}")
        

    def check_user_connection(self, group_name):
        self.socket.send_json({"request_type": "is_user_connected", "group_name": group_name, "user_uuid": self.uuid})

        response_str = self.socket.recv_string()
        print(response_str)


if __name__ == "__main__":
    user = User("User1", "tcp://localhost:2000")

    while True:
        print("1. Get Group List")
        print("2. Join Group")
        print("3. Create Group")
        print("4. Leave Group")
        print("5. Send Message")
        print("6. Get Messages")
        print("7. Check User Connection")
        print("8 . Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            user.get_group_list()
        elif choice == "2":
            group_name = input("Enter the name of the group to join: ")
            user.join_group(group_name)
        elif choice == "3":
            group_name = input("Enter the name of the new group: ")
            user.create_group(group_name)
        elif choice == "4":
            group_name = input("Enter the name of the group to leave: ")
            user.leave_group(group_name)
        elif choice == "5":
            group_name = input("Enter the name of the group to send a message: ")
            message = input("Enter your message: ")
            user.send_message(group_name, message)
        elif choice == "6":
            group_name = input("Enter the name of the group: ")
            timestamp = input("Enter the timestamp (optional): ")
            user.get_messages(group_name, timestamp)

        elif choice == "7":
            group_name = input("Enter the name of the group: ")
            user.check_user_connection(group_name)
        elif choice == "8":
            break
        else:
            print("Invalid choice. Please enter a valid option.")
