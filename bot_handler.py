from telethon import *
from configparser import ConfigParser

# Read config.ini
config = ConfigParser()
config.read('config.ini')

api_id = config.getint('Telegram_bot', 'api_id')
api_hash = config.get('Telegram_bot', 'api_hash')
bot_token = config.get('Telegram_bot', 'bot_token')
chat = config.getint('Telegram_bot', 'chat')

bot = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)

async def send_msg(msg):
    await bot.send_message(chat, msg)

async def send_pic(pic_name, capt=0):
    if capt==0:
        await bot.send_file(chat, pic_name)
    else:
        await bot.send_file(chat, pic_name, caption=capt)

async def send_file(file_name):
    file_name_dir = "down/" + file_name
    file_upload = await bot.upload_file(file_name_dir)
    await bot.send_file(chat, file_upload)