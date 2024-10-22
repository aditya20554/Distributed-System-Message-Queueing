import pika
import sys
import json

class Youtuber:
    def __init__(self, youtuber_name, video_name):
        self.youtuber_name = youtuber_name
        self.video_name = video_name

    def publishVideo(self):
        try:
            credentials = pika.PlainCredentials('jaysaraf', 'password') #Enter real password instead
            parameters = pika.ConnectionParameters('34.171.217.8',5672,'/',credentials)
            
            # Create a connection object with the RabbitMQ server
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Declare the exchange
            channel.exchange_declare(exchange='youtube', exchange_type='direct')

            # Create a message object with the required keys
            message = {
                'youtuber_name': self.youtuber_name,
                'video_name': self.video_name
            }

            # Convert message to JSON
            message_json = json.dumps(message)

            # Publish the message
            channel.basic_publish(
                exchange='youtube',
                routing_key='youtuber_requests',  # No routing key for direct exchange
                body=message_json.encode()  # Encode message as bytes
            )

            print("SUCCESS: Video published to YouTube server")
            connection.close()
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python Youtuber.py <YoutuberName> <VideoName>")
        sys.exit(1)
    
    youtuber_name = sys.argv[1]
    video_name = sys.argv[2]
    
    youtuber = Youtuber(youtuber_name, video_name)
    youtuber.publishVideo()
