import os
from auth import create_app 
from dotenv import load_dotenv 
load_dotenv()

config = os.environ.get("CONFIG") or "production"

app = create_app(config)
