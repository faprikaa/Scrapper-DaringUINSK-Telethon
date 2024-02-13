from telethon import TelegramClient

from util.config import API_ID, API_HASH, BOT_TOKEN

bot = TelegramClient('anon', API_ID, API_HASH).start(bot_token=BOT_TOKEN)