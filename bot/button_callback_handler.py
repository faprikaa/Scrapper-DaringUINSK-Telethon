import re

from telethon import events

import command_handler
from core.File import FileFromPost

bot = command_handler.bot


@bot.on(events.CallbackQuery(pattern=r"^download_file_\d+$"))
async def handle(event):
    post_id = event.data.decode().removeprefix("download_file_")
    print(post_id)
    file = FileFromPost(post_id)
    await file.send_file()
