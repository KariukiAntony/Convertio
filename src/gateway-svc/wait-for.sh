#! /bin/bash

HOST=rabbitmq
PORT=5672

if [ "$HOST" == "rabbitmq" ]; then
    echo "rabbitmq starting in a few ..."

    while ! nc -z "$HOST" "$PORT"; do
        echo "waiting for a tcp connection ..."
        sleep 2
    done

    echo "rabbitmql started"
else
  echo "Invalid rabbitmq host passed"
  exit 1

fi

exec "$@"
