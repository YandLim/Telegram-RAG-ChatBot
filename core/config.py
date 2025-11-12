# Import modules and libraries
from dotenv import load_dotenv
import os

# Setup
load_dotenv()
BOT_TOKEN = os.getenv("BOTTOKEN")
BOT_NAME = os.getenv("BOTNAME")

EMBED_MODEL = os.getenv("EMBEDMODEL")
LOCAL_MODEL = os.getenv("LOCALMODEL")

# Define file download folder
DOWNLOAD_FOLDER = "download_file/"
