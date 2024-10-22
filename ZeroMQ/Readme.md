                ZeroMQ Low-Level Group Messaging Application
This project implements a low-level group messaging application using ZeroMQ. It consists of a message server, group servers, and users interacting with each other in real-time. The message server maintains the list of groups and handles user requests to join or leave groups, while the group servers manage user group memberships and message handling within each group.

                        Architecture Overview
Message Server
Group List Maintenance: Maintains a list of groups identified by a unique identifier along with their IP addresses.
User Interaction: Handles user requests to join or leave groups, updating the group membership accordingly.

Group Servers
User Management: Maintains a list of users who are currently part of the group and manages user group memberships.
Message Handling: Stores messages sent by users and fetches relevant messages when requested.
Message Storage: Stores messages sent by users within each group, including timestamps and message content.

Users
Group Interaction: Users can join multiple groups simultaneously and leave groups when desired.
Message Operations: Users can write messages within the groups they are part of and fetch messages based on specified timestamps.


How to Run
Start the Message Server: Run the message_server.py script to start the message server, which listens for incoming requests from group servers and users.

Start Group Servers: Run the group_server.py script to start group servers. Each group server represents a specific group and manages group-related operations.

Interact with Users: Run the user.py script to interact with users. Users can perform actions such as getting the list of available groups, joining groups, sending messages, and fetching messages.



File Descriptions
message_server.py: Implements the message server that maintains the list of groups and handles user requests.
group_server.py: Implements group servers responsible for managing group operations.
user.py: Provides a user interface for interacting with the messaging application.



Dependencies
ZeroMQ: Install ZeroMQ library using pip install pyzmq.


Additional Notes
The application uses ZeroMQ for messaging between servers and clients.
Users can create new groups, join existing groups, and send/receive messages within groups.
Group servers handle group-specific operations such as user management and message handling.