from configparser import ConfigParser

import pytz
from telethon import TelegramClient

# Read config.ini
config = ConfigParser()
config.read('config.ini')

API_ID = config.getint('Telegram_bot', 'api_id')
API_HASH = config.get('Telegram_bot', 'api_hash')
BOT_TOKEN = config.get('Telegram_bot', 'bot_token')
CHAT_ID = config.getint('Telegram_bot', 'chat')

USERNAME = config.get('Login', 'username')
PASSWORD = config.get('Login', 'password')
OS_TYPE = config.get('Driver', 'OS')

TIMEZONE = pytz.timezone('Asia/Jakarta')
DOWNLOAD_PATH = config.get('Driver', 'download_path')