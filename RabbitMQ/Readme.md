YouTube-like Application with RabbitMQ
This project implements a simplified version of a YouTube-like application using RabbitMQ for communication between different components. The system comprises three main Python files: Youtuber.py, YoutubeServer.py, and User.py. Below is an overview of the project, its dependencies, and descriptions of each file.

Overview
The application allows YouTubers to publish videos, users to subscribe/unsubscribe to YouTubers, and receive real-time notifications whenever a subscribed YouTuber uploads a new video. Communication between components is facilitated by RabbitMQ message queues.

Dependencies
Python 3.x
RabbitMQ
RabbitMQ Python client library (pika)

File Descriptions
Youtuber.py : This file represents the YouTuber service, allowing YouTubers to publish videos by sending messages to the YouTube server.
YoutubeServer.py : This file sets up and runs the YouTube server, handling user login, subscription/unsubscription requests, and video upload requests.
User.py : This file represents the User service, allowing users to log in, subscribe/unsubscribe to YouTubers, and receive notifications.

Dependencies:
pika (RabbitMQ Python client library)
Code to follow:
pip install pika

For running on local machine username and password will is 'guest' by default and can be changed. But for running on gcp a new username and password needs to be created.

1. Message Queues and RabbitMQ Introduction
Message Queues are vital for modern distributed systems, enabling asynchronous communication between various components. RabbitMQ, a widely used message broker, facilitates communication between different parts of the system by adhering to the Advanced Message Queuing Protocol (AMQP).

Resources:
Introduction to Message Queues
RabbitMQ Official Tutorial
Learn more about RabbitMQ
Understanding message queues and RabbitMQ is crucial before delving into the assignment to make informed decisions regarding the types of queues and exchanges to use for communication between different application services.

2. Introduction to YouTube Service
In this programming assignment, we will develop a simplified version of a YouTube application using RabbitMQ. The system consists of three components:

2a. YouTuber
Allows YouTubers to publish videos on the YouTube server.
YouTubers can publish videos by sending messages to the YouTube server, including the video name and the YouTuber’s name.
2b. User
Users can subscribe or unsubscribe to YouTubers.
Receives real-time notifications whenever a subscribed YouTuber uploads a new video.
Users cannot directly communicate with YouTubers; communication happens only through the YouTube server.
2c. YouTubeServer
Consumes messages from Users and YouTubers.
Stores data about YouTubers, videos, users, and subscriptions.
Processes subscription and unsubscription requests from users.
Sends notifications to subscribers whenever a YouTuber uploads a new video.
3. Deliverables
3a. YoutubeServer.py
Sets up and runs the YouTube server.
Listens for and handles user login, subscription/unsubscription requests, and video upload requests.
Simultaneously consumes messages from both YouTubers and Users.
Provides methods for consuming user requests, YouTuber requests, and notifying users.
Example:

bash
Code to be followed:
# Run the server
$ python YoutubeServer.py
3b. youtuber.py
Represents the YouTuber service.
Takes YouTuber's name and video as command-line arguments.
Publishes the video to the YouTube server.
Example:

bash
Code to be followed:
# Publish a video
$ python youtuber.py TomScott "After ten years, it's time to stop weekly videos."
3c. User.py
Represents the User service.
Allows users to log in, subscribe/unsubscribe to YouTubers, and receive notifications.
Provides methods for updating subscriptions and receiving notifications.
Examples:

bash
Code to be followed:
# Log in, subscribe to a YouTuber, and receive notifications
$ python User.py username s TomScott

# Log in, unsubscribe to a YouTuber, and receive notifications
$ python User.py username u TomScott

# Log in and receive notifications
$ python User.py username
3d. README.md
Contains instructions to run the program.
Provides an overview of the project structure and components.
4. Flow of Service
Run YoutubeServer.py to start the server.
Run youtuber.py and User.py in any sequence simultaneously.
Users receive real-time notifications when subscribed YouTubers upload new videos.
Example for YoutubeServer.py : python YoutubeServer.py
Example for youtuber.py : python youtuber.py TomScott "After ten years"
Example for User.py : python User.py James
5. Running on Windows
Installation Steps for RabbitMQ
Download and install RabbitMQ from the official website: RabbitMQ Download

Follow the installation instructions provided on the RabbitMQ website for your specific version of Windows.

Start the RabbitMQ service.

Running the Application
Open Command Prompt.

Navigate to the directory containing the Python files.

Run each Python file using the python command as described in the examples above.

6. Running on Ubuntu
Installation Steps for RabbitMQ
Update the package index:
bash
Code to be followed:
$ sudo apt-get update
Install RabbitMQ server package:
bash
Code to be followed:
$ sudo apt-get install rabbitmq-server
Start the RabbitMQ service:
bash
Code to be followed:
$ sudo service rabbitmq-server start
Running the Application
Open Terminal.

Navigate to the directory containing the Python files.

Run each Python file using the python command as described in the examples above.

Notes
Data transfer between components should only occur via RabbitMQ message queues.
Architecture decisions regarding queues and exchanges are up to the developer.
Method parameters and functionalities can be adjusted as needed while maintaining the core functionality. Additional methods can be implemented as required.



