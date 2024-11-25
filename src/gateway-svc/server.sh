#! /bin/bash

function start_server(){
    echo "Starting the server ....."
    gunicorn --bind 0.0.0.0:5000 --workers 3 --threads 10 services:app
}

start_server