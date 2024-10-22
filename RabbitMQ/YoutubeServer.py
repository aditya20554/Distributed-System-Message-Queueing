import pika
import json

class YouTubeServer:
    def __init__(self):
        # Create a connection object with the RabbitMQ server
        credentials = pika.PlainCredentials('jaysaraf', 'password') #Enter real password instead
        
        # Create a connection parameters object
        parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
        
        # Create a connection object with the RabbitMQ server
        self.connection = pika.BlockingConnection(parameters)

        # Create a channel object from the connection
        self.channel = self.connection.channel()

        # Data storage
        self.users = {}
        self.youtubers = {}

        # Declare the exchange
        self.channel.exchange_declare(exchange='youtube', exchange_type='direct')  # Use direct exchange

        # Declare a queue for user requests
        self.channel.queue_declare(queue='user_requests')

        # Declare a queue for youtuber requests
        self.channel.queue_declare(queue='youtuber_requests')

        # Declare a queue for user notifications
        self.channel.queue_declare(queue='user_notify')

        self.channel.queue_declare(queue='error_notify')

        # Bind the user_requests queue to the exchange with the routing key 'user_subscription'
        self.channel.queue_bind(exchange='youtube', queue='user_requests', routing_key='user_requests')

        # Bind the user_notifications queue to the exchange with the routing key 'user_notifications'
        self.channel.queue_bind(exchange='youtube', queue='user_notify', routing_key='user_notifications')

        self.channel.queue_bind(exchange='youtube', queue='error_notify', routing_key='message_error')

        # Bind the youtuber_requests queue to the exchange with the routing key 'youtuber_requests'
        self.channel.queue_bind(exchange='youtube', queue='youtuber_requests', routing_key='youtuber_requests')

        # Start consuming messages from the user_requests queue
        self.channel.basic_consume(queue='user_requests', on_message_callback=self.consume_user_requests, auto_ack=True)

        # Start consuming messages from the youtuber_requests queue
        self.channel.basic_consume(queue='youtuber_requests', on_message_callback=self.consume_youtuber_requests, auto_ack=True)

        # Start consuming messages
        print("YouTube server is running...")
        self.channel.start_consuming()

    def consume_user_requests(self, ch, method, properties, body):
        # Parse the body as a JSON object
        request = json.loads(body)
        # print(type(request))
        if 'subscribe' in request.keys() and request['subscribe'] == True:
            sub = "subscribe" 
        else:
            sub = "unsubscribe" 

        # Check if it is a login or a subscription request
        if 'user' in request.keys() and len(request) == 1:
            # Get the user name
            username = request.get('user')
            # Print a message
            print(f"{username} logged in")
            # Add the user to the data dictionary if not already there
            if username not in self.users:
                self.users[username] = {'subscription': []}

        elif 'subscribe' in request:
            # Get the user name, the youtuber name, and the action
            username = request.get('user')
            youtuber_name = request['youtuber']
            sub = request['subscribe']
            
            print(f"The request sent by user is: {request['user']} wants to {sub} from {request['youtuber']}")

            if sub:
                action = 's'
            else:
                action = 'u'

            # Print a message
            print(f"{username} {action} to {youtuber_name}")

            if youtuber_name not in self.youtubers:
                error_message = {'status': 'error', 'message': f"Youtuber '{youtuber_name}' does not exist."}
                self.send_error_message(error_message)
                return

            # Update the user's subscriptions accordingly
            if action == 's':
                # Add the youtuber to the user's subscriptions if not already there
                if youtuber_name not in self.users.get(username, {}).get('subscription', []):
                    if username in self.users:
                        self.users[username]['subscription'].append(youtuber_name)
                        error_message = {'status': 'no error', 'message': f'Successfully {action} to {youtuber_name}'}
                        self.send_error_message(error_message)
                        return
                    else:
                        self.users[username] = {'subscription': [youtuber_name]}
                        # print(self.users)
                        error_message = {'status': 'no error', 'message': f'Successfully {action} to {youtuber_name}'}
                        self.send_error_message(error_message)
                        return
            elif action == 'u':
                # Remove the youtuber from the user's subscriptions if present
                if youtuber_name in self.users.get(username, {}).get('subscription', []):
                    self.users.get(username, {}).get('subscription', []).remove(youtuber_name)

                    error_message = {'status': 'no error', 'message': f'Successfully {action} to {youtuber_name}'}
                    self.send_error_message(error_message)
                    return

                if youtuber_name in self.youtubers:
                    error_message = {'status': 'error', 'message': f"{username} had never subscribed to Youtuber '{youtuber_name}'."}
                    self.send_error_message(error_message)
                    return
            # Checking whether data is getting stored properly or not
        # print("Users dictionary:", self.users)

    def consume_youtuber_requests(self, ch, method, properties, body):
        # Parse the body as a JSON object
        video_info = json.loads(body)

        # Get the youtuber name and the video name
        youtuber_name = video_info.get('youtuber_name')
        video_name = video_info.get('video_name')

        # Print a message indicating that a message has been received from Youtuber.py
        print(f"Received message from Youtuber: {youtuber_name} about the video {video_name}")

        # Print a message
        if youtuber_name:
            if youtuber_name != "" and video_name != "":
                print(f"{youtuber_name} uploaded {video_name}")

        # Add the video to the youtuber's data dictionary
        if youtuber_name not in self.youtubers:
            self.youtubers[youtuber_name] = {'videos': []}
        self.youtubers[youtuber_name]['videos'].append(video_name)
        # Checking whether data is getting store properly or not
        # print(self.youtubers[youtuber_name]['videos'])
        # Checking whether data is getting stored properly or not
        # print("Youtubers dictionary:", self.youtubers)

        # Call the notify_users method to send notifications to the subscribers
        self.notify_users(youtuber_name, video_name)

    def notify_users(self, youtuber_name, video_name):
        # Loop through the users data dictionary
        for user_name, user_info in self.users.items():
            # print(user_info)
            # Check if the user is subscribed to the youtuber
            if youtuber_name in user_info['subscription']:
                # Create a message object with the notification details as a JSON string
                message = json.dumps({'youtuber_name': youtuber_name, 'video_name': video_name})
                # print("The message being sent is", message)
                # Publish the message to the exchange with the routing key as the user's name
                self.channel.basic_publish(exchange='youtube', routing_key='user_notifications', body=message)

    def send_error_message(self, error_message):
        # Create a message object with the error details as a JSON string
        message = json.dumps(error_message)
        print("Error message sent:", message)
        # Publish the error message to the exchange with the routing key 'message_error'
        self.channel.basic_publish(exchange='youtube', routing_key='message_error', body=message)


if __name__ == "__main__":
    # Instantiate the YouTubeServer object
    youtube_server = YouTubeServer()
