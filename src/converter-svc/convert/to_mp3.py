import json, os, pika
import tempfile 
from bson.objectid import ObjectId
import moviepy.editor
from dotenv import load_dotenv
load_dotenv()

def start(channel, fs_videos, fs_mp3s, message):
    message = json.loads(message)
    tf = tempfile.NamedTemporaryFile()
    video = fs_videos.get(ObjectId(message["video_fid"]))
    tf.write(video.read())
    # covert the video into audio
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()
    # convert the video to audio
    audio_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(audio_path)
    # save the contents of the audio path in mongodb
    with open(audio_path, "rb") as audio_file:
        mp3_fid = fs_mp3s.put(audio_file.read())
    os.remove(audio_path)
    message["mp3_fid"] = str(mp3_fid)
    print(f"This is the mp3 fid: {str(mp3_fid)}")

    try:
        channel.queue_declare(queue=os.environ.get("MP3_QUEUE"), durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        return None
    except Exception as error:
        fs_mp3s.delete(mp3_fid)
        return "Failed to publish"
    