#! /bin/bash 

set -e

function start_server(){
   echo "starting the server for the auth service ....." 
   gunicorn --bind 0.0.0.0:8000 --workers 1 --threads 3 wsgi:app
}

start_server