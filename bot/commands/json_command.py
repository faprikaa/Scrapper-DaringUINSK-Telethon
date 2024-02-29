import asyncio

from telethon import events

from core.bot import bot
from core.classes.Post import Post
from util.config import CHAT_ID
from util.json_util import load_saved_data, get_saved_data_by_post_id


@bot.on(events.NewMessage(pattern='/list'))
async def handler(event):
    datas = load_saved_data()
    msg = "Saved Data : \n"
    for data in datas:
        msg += f"`{data}`\n"
    bot_msg = await bot.send_message(CHAT_ID, msg)
    await asyncio.sleep(600)
    await bot.delete_messages(CHAT_ID, bot_msg)


@bot.on(events.NewMessage(pattern='/get(?:\s|$)(.*)'))
async def handler(event):
    post_id = str(event.pattern_match.group(1)).strip()
    if post_id == "":
        await bot.send_message(CHAT_ID, "Masukkan ID Postingan, contoh `/get 123321`")
        return
    elif not get_saved_data_by_post_id(post_id):
        await bot.send_message(CHAT_ID, f"Data Postingan `{post_id}` tidak ditemukan")
        return
    msg = await bot.send_message(CHAT_ID, f"Memproses Postingan `{post_id}`")
    post = Post(post_id, from_json=True)
    await post.send()
    await bot.delete_messages(CHAT_ID, msg)
