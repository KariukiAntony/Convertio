FROM python:3.8-slim-bullseye

RUN apt-get update && apt-get install -y --no-install-recommends --no-install-suggests build-essential libpq-dev python3-dev && pip install --no-cache-dir --upgrade pip

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update && apt install -y netcat

COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
COPY ./wait-for.sh /app/
RUN chmod +x ./wait-for.sh

ENTRYPOINT ["./wait-for.sh"]
