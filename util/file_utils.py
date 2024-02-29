from core.bot import bot
from core.classes.File import File
from util.config import CHAT_ID


async def send_files(file_elements, overwrite=False, reply_msg_id=None):
    if reply_msg_id is None:
        msg = await bot.send_message(CHAT_ID, "Downloading file...")
    else:
        msg = await bot.send_message(CHAT_ID, "Downloading file...", reply_to=reply_msg_id)

    try:
        for file_element in file_elements:
            file = File(file_element)
            await file.send_file(overwrite=overwrite, progress_msg=msg)
    finally:
        await bot.delete_messages(CHAT_ID, [msg])