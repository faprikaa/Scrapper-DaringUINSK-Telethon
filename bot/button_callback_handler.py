import re

from telethon import events
from telethon.events.callbackquery import CallbackQuery
from core.bot import bot
from core.classes.File import FileFromPost
from util.config import CHAT_ID


@bot.on(events.CallbackQuery(pattern=r"^download_file_\d+$"))
async def handle(event: CallbackQuery.Event):
    post_id = event.data.decode().removeprefix("download_file_")
    file = FileFromPost(post_id)
    await file.send_file()


@bot.on(events.CallbackQuery(pattern="hapus"))
async def handle(event: CallbackQuery.Event):
    await bot.delete_messages(entity=CHAT_ID, message_ids=event.message_id)
