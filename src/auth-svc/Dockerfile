FROM python:3.8-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests build-essential libpq-dev python3-dev && pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app

EXPOSE 8000

RUN chmod +x ./server.sh
