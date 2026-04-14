import os
from dotenv import load_dotenv

load_dotenv()

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

USER_VIDEO_LIMIT = 10
COMPETITOR_VIDEO_LIMIT = 20
COMPETITOR_AUTO_LIMIT = 50
DAYS_LOOKBACK = 90
