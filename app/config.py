import os
from dotenv import load_dotenv

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8000))
DB_PATH = os.getenv("DB_PATH", "history.db")


