import sys, os, pika
from send import notification
from dotenv import load_dotenv

load_dotenv()

def main():
    print("Making connection ...")
    print(os.environ.get("RABBITMQ_USER"))
    print(os.environ.get("RABBITMQ_PASS"))
    print(os.environ.get("RABBITMQ_HOST"))
    # RabbitMQ connection parameters
    credentials = pika.PlainCredentials(
        os.environ.get("RABBITMQ_USER", "guest"),
        os.environ.get("RABBITMQ_PASS", "guest")
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ.get("RABBITMQ_HOST", "localhost"),
            credentials=credentials,
            heartbeat=0
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=os.environ.get("MP3_QUEUE"), durable=True)
    print("connected ..")

    def callback(channel, method, properties, body):
        error = notification(body)
        if error:
            channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"), on_message_callback=callback, auto_ack=False
    )

    print("[Notification] Waiting for messages. press CTRL+C to quit ...")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            print("Interrupted. Exiting ....")
            sys.exit(0)
        except SystemExit:
            os._exit(0)
