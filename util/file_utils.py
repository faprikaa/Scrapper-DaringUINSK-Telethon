from core.bot import bot
from core.classes.File import File
from util.config import CHAT_ID


async def send_files(file_elements, overwrite=False, reply_msg_id=None):
    msg = None
    i = 1
    for file_element in file_elements:
        try:
            if reply_msg_id is None:
                msg = await bot.send_message(CHAT_ID, f"Downloading file ke-{i}...")
            else:
                msg = await bot.send_message(CHAT_ID, f"Downloading file ke-{i}...", reply_to=reply_msg_id)
            file = File(file_element)
            await file.send_file(overwrite=overwrite, progress_msg=msg)
            i += 1
        finally:
            await bot.delete_messages(CHAT_ID, [msg])
