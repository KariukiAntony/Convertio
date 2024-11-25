import os, gridfs, pika, json
from flask import Flask, jsonify, send_file
from flask import request
from storage import utils
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from auth_svc import access

app = Flask(__name__)

mongo_video = PyMongo(app=app, uri=os.environ.get("MONGODB_VIDEOS_URI"))
mongo_mp3 = PyMongo(app=app, uri=os.environ.get("MONGODB_MP3_URI"))
fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

try:
    credentials = pika.PlainCredentials(os.environ.get("RABBITMQ_USER", "guest"), os.environ.get("RABBITMQ_PASS", "guest"))
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.environ.get("RABBITMQ_HOST"), credentials=credentials, heartbeat=0)
    )
    print("connected to rabbitmq successfully ...")
    channel = connection.channel()

except Exception as e:
    print(f"Error connecting to rabbitmq: {str(e)}")

@app.get("/api/healthcheck")
def healthcheck():
    return jsonify({"Message": "api is up and running ..."})

@app.route("/api/v1/auth/register", methods=["POST"])
def register():
    response = access.register(request)
    return jsonify(response.json()), response.status_code


@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    response = access.login(request)
    return jsonify(response.json()), response.status_code


@app.route("/api/v1/upload", methods=["POST"])
def upload():
    token, error = access.validate(request)
    print(token, error)
    if token:
        token = json.loads(token)
        if len(request.files) > 1 or len(request.files) < 1:
            return "Exactly one file is required ....", 400
        for name, file in request.files.items():
            print(f"This is the file {file}")
            # upload the video in the db and produce a message
            error = utils.upload(file, fs_videos, channel, {"username": token.get("email")})
            if error:
                return f"failed with error: {str(error)}", 502
            return "Video uploaded successfully ...", 200

    else:
        return error, 401


@app.route("/api/v1/download")
def download():
    token, error = access.validate(request)
    if token:
        mp3_fid = request.args.get("fid")
        print(mp3_fid)
        if not mp3_fid:
            return "The music fid is required", 400
        try:
            mp3_out = fs_mp3s.get(ObjectId(mp3_fid))
            print(mp3_out)
            return send_file(mp3_out, download_name=f"{mp3_fid}.mp3")
        except Exception as error:
            return f"Internal server error: {error}", 502
    else:
        return error, 401

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")