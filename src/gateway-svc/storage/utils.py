import json, pika
import os
from dotenv import load_dotenv
load_dotenv()

queue = os.environ.get("VIDEO_QUEUE")
def upload(file, fs, channel, access):
    try:
        video_fid = fs.put(file)
    except Exception as error:
        return f"Internal server error, fs level: {str(error)}", 500

    message = {"video_fid": str(video_fid), "mp3_fid": None, "username": access["username"]}

    try:
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )

    except Exception as error:
        # Roll back MongoDB storage if there's a RabbitMQ error
        fs.delete(video_fid)
        return f"Internal server error, rabbitmq level: {str(error)}", 500
