from configparser import ConfigParser

import pytz

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

SENIN = config.get('Jadwal', 'Senin')
SELASA = config.get('Jadwal', 'Selasa')
RABU = config.get('Jadwal', 'Rabu')
KAMIS = config.get('Jadwal', 'Kamis')
JUMAT = config.get('Jadwal', 'Jumat')

USE_SCHEDULER = config.get('Jadwal', 'scheduler')
LOOPING_INTERVAL = config.get('Jadwal', 'looping_interval')
LOOPING_SCHEDULER_INTERVAL = config.getint('Jadwal', 'looping_scheduler_interval')

TIMEZONE = pytz.timezone('Asia/Jakarta')
DOWNLOAD_PATH = config.get('Driver', 'download_path')

CHECK_COMMENT_EVERY_POST = config.getboolean('Other', 'cek_comment_every_post')
AUTO_HADIR = config.getboolean('Other', 'auto_hadir')
MINIMAL_COMMENT = config.getint('Other', 'minimal_comment')
