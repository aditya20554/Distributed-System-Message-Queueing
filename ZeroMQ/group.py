import zmq
import threading
import json
from datetime import datetime

class GroupServer:
    def __init__(self, name,address):
        self.name = name
        self.address = address
        # self.address = address 
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(self.address)
        self.users = set()  # Set to store user UUIDs
        self.messages = []  # List to store messages {timestamp, user_uuid, content}
        

    def register_with_message_server(self):
        registration_socket = self.context.socket(zmq.REQ)
        registration_socket.connect("tcp://localhost:2000")

        request = {"request_type": "register_group_server", "group_name": self.name, "group_address": self.address.split(":")[-1]}

        registration_socket.send_json(request)
        response = registration_socket.recv_string()
        print(f"Server prints: {response}")


    def handle_join_request(self, user_uuid):
        self.users.add(user_uuid)
        print("JOIN REQUEST FROM : ", user_uuid)
        return "SUCCESS"

    def handle_leave_request(self, user_uuid):
        if user_uuid in self.users:
            self.users.discard(user_uuid)
            print("LEAVE REQUEST FROM : ",user_uuid)
            return "SUCCESS"
        else:
            return "User Not a member of the group."

    def handle_get_messages(self, user_uuid, timestamp=None):
        if user_uuid in self.users:
            if timestamp:
                relevant_messages = [msg for msg in self.messages if msg['timestamp'] >= timestamp]
            else:
                relevant_messages = self.messages
            print("MESSAGE REQUEST FROM : ",user_uuid)
            return relevant_messages
        else : 
            print("User not a member of this group.")
            return "FAIL"
    

    def handle_send_message(self, user_uuid, message_content):
        if user_uuid in self.users:
            timestamp = datetime.now().isoformat()
            self.messages.append({'timestamp': timestamp, 'user_uuid': user_uuid, 'content': message_content})
            print("MESSAGE SEND FROM User: ", self.messages[-1]["user_uuid"])
            return "SUCCESS - Message received and added to group"
        else:
            print("User not a member of this group.")
            return "FAIL"

    def handle_check_user_connection(self, user_uuid):
        if user_uuid in self.users:
            return "Connected"
        else:
            return "Not Connected"
    
    def handle_create_group(self, group_name,group_address):
        new_address = f"tcp://*:{group_address}"  # Generate new address for the new group server
        threading.Thread(target=start_group_server,args=(group_name, new_address)).start()
        return f"SUCCESS - Group : '{group_name}' created at port {group_address}"



def start_group_server(name , address):
    server = GroupServer(name , address)
    server.register_with_message_server()
    while True:
        message = server.socket.recv_json()
        if message["request_type"] == "join_group":
            response = server.handle_join_request(message["user_uuid"])
        elif message["request_type"] == "leave_group":
            response = server.handle_leave_request(message["user_uuid"])
        elif message["request_type"] == "get_messages":
            timestamp = message.get("timestamp")
            response = server.handle_get_messages(message["user_uuid"], timestamp)
        elif message["request_type"] == "send_message":
            response = server.handle_send_message(message["user_uuid"], message["message_content"])
        elif message["request_type"] == "is_user_connected":
            response = server.handle_check_user_connection(message["user_uuid"])
        elif message["request_type"] == "create_group":
            response = server.handle_create_group(message["group_name"],message["group_address"])
        else:
            response = "INVALID REQUEST"
        server.socket.send_string(json.dumps(response))

if __name__ == "__main__":
    
    
    group_servers = [
        
        threading.Thread(target=start_group_server, args=("Group1", "tcp://*:3000")),
        threading.Thread(target=start_group_server, args=("Group2", "tcp://*:3001")),   
        threading.Thread(target=start_group_server, args=("Group3", "tcp://*:3002")),   
        threading.Thread(target=start_group_server, args=("Group4", "tcp://*:3003")),   
        threading.Thread(target=start_group_server, args=("Group5", "tcp://*:3004")),   
    ]

    for server_thread in group_servers:
        server_thread.start()

   
    for server_thread in group_servers:
        server_thread.join()
    input("Press Enter to exit.")
