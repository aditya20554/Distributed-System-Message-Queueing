Online Shopping Platform Implementation Using gRPC
Overview
This repository contains the implementation of an online shopping platform using gRPC for communication between different components. The platform consists of three main components: Market (Central Platform), Seller, and Buyer. The Market serves as the central hub connecting sellers and buyers, while the Seller manages their items and transactions, and the Buyer searches for and purchases items.

Dependencies
Python 3.x
gRPC
Protocol Buffers
File Descriptions
market.py: Python script implementing the Market (Central Platform) functionalities.
market.proto: Protocol Buffer definition file containing all the definitions for communication between Market and Clients (Sellers/Buyers).
market_pb2.py: Python module generated from market.proto for Market message types.
market_pb2_grpc.py: Python module generated from market.proto for Market gRPC service.
seller.py: Python script implementing the Seller functionalities.
buyer.py: Python script implementing the Buyer functionalities.
Installation
Install gRPC and Protocol Buffers:
Code to follow:
pip install grpcio grpcio-tools
Generating gRPC Files from Protobuf
To generate Python files from the .proto file, use the following command:


Code to follow:
python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. market.proto
Running the Code
Start Market (Central Platform):

Code to follow:
python market.py
Start Seller Instances:

Code to follow:
python seller.py
Start Buyer Instances:

Code to follow:
python buyer.py
Ensure that you follow the specified communication protocol and print statements for each functionality to ensure proper evaluation.

Additional Information
Each component communicates with others using gRPC, ensuring efficient and reliable communication.
Protocol Buffers are used for defining the message formats exchanged between different components, providing a language-neutral, platform-neutral way to define structured data schemas.
The Market maintains seller accounts, item details, transaction logs, and notifications to buyers and sellers.
Sellers manage their items by registering, adding, updating, deleting, and viewing their products.
Buyers search for items, purchase them, wishlist items for notifications, and rate items.