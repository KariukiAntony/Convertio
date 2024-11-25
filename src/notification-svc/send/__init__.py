from email.message import EmailMessage
import json, os, smtplib
from dotenv import load_dotenv
load_dotenv()

def notification(message):
    message = json.loads(message)
    print(message)
    mp3_fid = message["mp3_fid"]
    sender_address = os.environ.get("GMAIL_ADDRESS")
    sender_password = os.environ.get("GMAIL_PASSWORD")
    receiver_address = message["username"]
    if not sender_address or not sender_password:
        raise ValueError("GMAIL_ADDRESS and GMAIL_PASSWORD environment variables must be set")

    msg = EmailMessage()
    msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!")
    msg["Subject"] = "MP3 Download"
    msg["From"] = sender_address
    msg["To"] = receiver_address

    session = smtplib.SMTP("smtp.gmail.com", 587)
    session.starttls()
    session.login(sender_address, sender_password)
    session.send_message(msg, sender_address, receiver_address)
    session.quit()
    print("Mail Sent successfully ...")

