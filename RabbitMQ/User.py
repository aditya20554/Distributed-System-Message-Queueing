import pika
import json
import sys

# Get the command line arguments
user_name = sys.argv[1]
if len(sys.argv) == 4:
    action = sys.argv[2]
    youtuber_name = sys.argv[3]

credentials = pika.PlainCredentials('jaysaraf', 'password') #Enter real password instead
parameters = pika.ConnectionParameters(host='34.171.217.8',port=5672,virtual_host='/',credentials=credentials)

# Create a connection object with the RabbitMQ server
connection = pika.BlockingConnection(parameters)

# Create a channel object from the connection
channel = connection.channel()

# Declare an exchange object with the channel
channel.exchange_declare(exchange='youtube', exchange_type='direct')  # Ensure exchange type matches with YoutubeServer.py

# Declare a queue object with the channel
result = channel.queue_declare(queue='', exclusive=True)
user_notification_queue_name = result.method.queue

# Bind the queue to the exchange with the correct routing key
channel.queue_bind(exchange='youtube', queue=user_notification_queue_name, routing_key='user_notifications')

# Declare a queue object with the channel for error notifications
error_result = channel.queue_declare(queue='', exclusive=True)
error_notification_queue_name = error_result.method.queue
# Bind the queue to the exchange with the correct routing key for error notifications
channel.queue_bind(exchange='youtube', queue=error_notification_queue_name, routing_key='message_error')

# Define a callback function that will be executed when a message is received from the queue
def callback(ch, method, properties, body):
    # Parse the message as a JSON object
    message = json.loads(body)
    # print(f"Received message: {message}")
    
    # Check if the message is a notification from YoutubeServer.py
    if 'youtuber_name' in message and 'video_name' in message:
        # print("Received a notification message from YoutubeServer.py")
        youtuber_name = message.get('youtuber_name')
        video_name = message.get('video_name')
        print(f"Received message: {youtuber_name} uploaded {video_name}")

# Define a callback function for error notifications
def error_notification_callback(ch, method, properties, body):
    # Parse the message as a JSON object
    error_message = json.loads(body)
    print(f"Received error message: {error_message}")
    # Print the error message

    if(error_message['status'] == 'error'):
        print("Error:", error_message['message'])
    else:
        print(f'Successfully {action} to {youtuber_name}')

    # If there was an error, print a success message only if the action was to subscribe (len(sys.argv) == 4)

# If the user wants to subscribe or unsubscribe to a youtuber
if len(sys.argv) == 4:
    # Create a message object with the user name, the youtuber name, and the subscribe flag as a JSON string
    message = json.dumps({'user': user_name, 'youtuber': youtuber_name, 'subscribe': action == 's'})
    # Publish the message to the exchange with the routing key as 'user_requests'
    channel.basic_publish(exchange='youtube', routing_key='user_requests', body=message)

    # Start consuming messages from the error notification queue
    channel.basic_consume(queue=error_notification_queue_name, on_message_callback=error_notification_callback, auto_ack=True)

    # Print a success message
    # print(f'Successfully {action} to {youtuber_name}')
elif len(sys.argv) == 2:
    message = json.dumps({'user': user_name})
    # Publish the message to the exchange with the routing key as 'user_requests'
    channel.basic_publish(exchange='youtube', routing_key='user_requests', body=message)
    # Print a message indicating the message being sent to YoutubeServer.py
    print('Message sent to YoutubeServer.py:', message)

# Start consuming messages from the queue
channel.basic_consume(queue=user_notification_queue_name, on_message_callback=callback, auto_ack=True)

# Close the connection when the user exits the program
try:
    channel.start_consuming()
except KeyboardInterrupt:
    connection.close()
