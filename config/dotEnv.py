import json
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
TENANT_ID = os.getenv("TENANT_ID")
EBOTIFY_URL = os.getenv("EBOTIFY_URL")
IS_LIVE_AGENT = json.loads(os.getenv("IS_LIVE_AGENT"))
