import pika
import pika.credentials
from pymongo import MongoClient
import sys, os
from gridfs import GridFS
from convert import to_mp3
from dotenv import load_dotenv
load_dotenv()

credentials = pika.PlainCredentials(os.environ.get("RABBITMQ_USER", "guest"), os.environ.get("RABBITMQ_PASS", "guest"))

def main():
    client = MongoClient(os.environ.get("MONGODB_URL"))
    db_videos = client.videos  # videos db
    db_mp3s = client.mp3s # mp3 db
    
    fs_videos = GridFS(db_videos)
    fs_mp3s = GridFS(db_mp3s)

    # rabbitmq connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST"), credentials=credentials, heartbeat=0)
    )
    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get("VIDEO_QUEUE"), durable=True)
    
    def callback(channel, method, properties, body):
        error = to_mp3.start(channel, fs_videos, fs_mp3s, body)
        if error:
            channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback, auto_ack=False
    )
    print("[Converter] Waiting for messages. press CTRL+C to quit ...")
    
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("Interrupted. Exiting .....")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
