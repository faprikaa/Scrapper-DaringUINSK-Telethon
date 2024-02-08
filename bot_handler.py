from telethon import *
from configparser import ConfigParser
from telethon.errors import *

# Read config.ini
config = ConfigParser()
config.read('config.ini')

api_id = config.getint('Telegram_bot', 'api_id')
api_hash = config.get('Telegram_bot', 'api_hash')
bot_token = config.get('Telegram_bot', 'bot_token')
chat = config.getint('Telegram_bot', 'chat')

bot = TelegramClient('anon', api_id, api_hash).start(bot_token=bot_token)

async def send_msg(msg):
    try:
        await bot.send_message(chat, msg)
    except MessageTooLongError:
        print(len(msg))
        print(msg)
        msg = msg[:2056]
        await bot.send_message(chat, msg)

async def send_pic(pic_name, capt=False):
    if capt:
        try:
            await bot.send_file(chat, pic_name, caption=capt)
        except MediaCaptionTooLongError:
            print(len(capt))
            capt2 = capt[:1024]
            await bot.send_file(chat, pic_name, caption=capt2)
    else:
        await bot.send_file(chat, pic_name)

async def send_file(fpath):
    file_upload = await bot.upload_file(fpath)
    await bot.send_file(chat, file_upload)