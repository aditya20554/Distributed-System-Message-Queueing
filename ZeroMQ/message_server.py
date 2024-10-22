import zmq
import threading
import json

class MessageServer:
    def __init__(self, address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(address)
        self.groups = {}  # Dictionary to store groups {group_name: group_address}


    def handle_group_list_request(self):
        return json.dumps(self.groups) 
    

    def handle_register_group_server(self,group_name ,group_address):
        self.groups[group_name] = f"localhost:{group_address}"
        print(f"JOIN REQUEST FROM {group_name} [{group_address}]")
        return "SUCCESS"
        


    def handle_join_request(self, group_name ,user_uuid):
        if group_name not in self.groups:
            print("Group not found")
            return "FAIL"
        else:
            group_address = self.groups[group_name]
            group_socket = self.context.socket(zmq.REQ)
            group_socket.connect(f"tcp://{group_address}")
            group_socket.send_json({"request_type": "join_group", "user_uuid": user_uuid})
            response = group_socket.recv_string()
            return response



    def handle_leave_request(self, group_name, user_uuid):
        if group_name in self.groups:
            group_address = self.groups[group_name]
            group_socket = self.context.socket(zmq.REQ)
            group_socket.connect(f"tcp://{group_address}")
            group_socket.send_json({"request_type": "leave_group", "user_uuid": user_uuid})
            response = group_socket.recv_string()
            return response
        else:
            return "FAIL"

    

    def handle_send_message(self, group_name, user_uuid, message_content):
        if group_name in self.groups:
            # Forward message to the corresponding group server
            group_address = self.groups[group_name]
            group_socket = self.context.socket(zmq.REQ)
            group_socket.connect(f"tcp://{group_address}")
            group_socket.send_json({"request_type": "send_message", "user_uuid": user_uuid, "message_content": message_content})
            response = group_socket.recv_string()
            return response
        else:
            return "FAIL - Group not found"



    def handle_get_messages(self, group_name, user_uuid,timestamp):
        if group_name in self.groups:
            # Forward message to the corresponding group server
            group_address = self.groups[group_name]
            group_socket = self.context.socket(zmq.REQ)
            group_socket.connect(f"tcp://{group_address}")
            group_socket.send_json({"request_type": "get_messages", "user_uuid": user_uuid , "timestamp": timestamp})
            messages = group_socket.recv_json()
            return json.dumps(messages)
        else:
            return json.dumps()



    def handle_check_user_connection(self, group_name, user_uuid):
        if group_name in self.groups:
            check_request = {"request_type": "is_user_connected", "user_uuid": user_uuid}
            context = zmq.Context()
            group_address = self.groups[group_name]
            group_socket = context.socket(zmq.REQ)
            group_socket.connect(f"tcp://{group_address}")
            group_socket.send_json(check_request)
            response = group_socket.recv_string()
            group_socket.close()
            return response
        else:
            return "FAIL - Group not found"


      
        
    def handle_create_group(self, group_name):
        if group_name not in self.groups:
            
            group_socket = self.context.socket(zmq.REQ)
            group_socket.connect("tcp://localhost:3000") 
            group_address = len(self.groups) + 3000 
            request = {"request_type": "create_group", "group_name": group_name,"group_address":group_address}
            group_socket.send_json(request)
            response = group_socket.recv_string()
            group_socket.close()
            return response
        else:
            print("Group already exists")
            return "FAIL"


def start_message_server():
    server = MessageServer("tcp://*:2000")
    while True:
        message = server.socket.recv_json()
        
        if message["request_type"] == "register_group_server":
            response = server.handle_register_group_server(message["group_name"] , message["group_address"])
        elif message["request_type"] == "join_group":
            response = server.handle_join_request(message["group_name"],message["user_uuid"])
        elif message["request_type"] == "leave_group":
            response = server.handle_leave_request(message["group_name"],message["user_uuid"])
        elif message["request_type"] == "get_group_list":
            response = server.handle_group_list_request()
        elif message["request_type"] == "send_message":
            response = server.handle_send_message(message["group_name"], message["user_uuid"], message["message_content"])
        elif message["request_type"] == "get_messages":
            response = server.handle_get_messages(message["group_name"], message["user_uuid"] , message["timestamp"])
        elif message["request_type"] == "is_user_connected":
            response = server.handle_check_user_connection(message["group_name"], message["user_uuid"])
        elif message["request_type"] == "create_group":
            response = server.handle_create_group(message["group_name"])
        else:
            response = "INVALID REQUEST"
    
        server.socket.send_string(str(response))

if __name__ == "__main__":
    threading.Thread(target=start_message_server, daemon=True).start()
    input("Press Enter to exit.\n")
