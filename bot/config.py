import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"

ADMIN_ID = os.getenv("ADMIN_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")
EXEMPT_CHANNEL_ID = os.getenv("EXEMPT_CHANNEL_ID")
WHITE_CHANNEL_ID = os.getenv("WHITE_CHANNEL_ID")
CMC_API_KEY = os.getenv("COINMARKETCAP_KEY") or os.getenv("CMC_API_KEY")
