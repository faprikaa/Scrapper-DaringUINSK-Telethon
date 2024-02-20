from telethon.errors import *


async def send_msg(msg):
    try:
        await bot.send_message(chat, msg)
    except MessageTooLongError:
        print(len(msg))
        print(msg)
        msg = msg[:2056]
        await bot.send_message(chat, msg)


async def send_pic(pic_name, capt=None):
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
    msg = await bot.send_message(chat, "Uploading...")

    async def callback(current, total):
        await bot.edit_message(msg, message=f"Uploaded: {format(current / total, '.2%')}")

    file_upload = await bot.upload_file(fpath, progress_callback=callback)
    await bot.send_file(chat, file_upload)
    await bot.delete_messages(chat, msg)
