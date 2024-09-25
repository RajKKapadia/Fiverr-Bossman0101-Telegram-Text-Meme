import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TELEGRAM_BOT_API_KEY = os.getenv("TELEGRAM_BOT_API_KEY")
SUPERMEME_API_KEY = os.getenv("SUPERMEME_API_KEY")
