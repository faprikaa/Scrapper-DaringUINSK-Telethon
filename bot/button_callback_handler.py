import asyncio

from telethon import events
from telethon.events.callbackquery import CallbackQuery

from core.bot import bot
from core.classes.Post import Post
from function.scheduler import send_loop_msg
from util.config import CHAT_ID
from util.file_utils import send_files
from util.json_util import get_saved_data_by_post_id
from utils import generate_caption


@bot.on(events.CallbackQuery(pattern=r"^download_file_\d+$"))
async def handle(event: CallbackQuery.Event):
    post_id = event.data.decode().removeprefix("download_file_")
    post_data = get_saved_data_by_post_id(post_id)
    if not post_data:
        msg = await event.reply("Data postingan tidak ditemukan di penyimpanan")
        await asyncio.sleep(300)
        await bot.delete_messages(CHAT_ID, msg)
        return
    if post_data["total_file"] > 0:
        file_elements = post_data["file_elements"]
        await send_files(file_elements)


@bot.on(events.CallbackQuery(pattern=r"^full_capt_\d+$"))
async def handle(event: CallbackQuery.Event):
    post_id = event.data.decode().removeprefix("full_capt_")
    post = Post(post_id)
    capt = generate_caption(post.to_json(), True)
    buttons = post.generate_button(True)
    await bot.edit_message(
        entity=CHAT_ID,
        message=event.message_id,
        file=post.pic_name,
        text=capt,
        buttons=buttons
    )


@bot.on(events.CallbackQuery(pattern=r"^mini_capt_\d+$"))
async def handle(event: CallbackQuery.Event):
    post_id = event.data.decode().removeprefix("mini_capt_")
    post = Post(post_id)
    capt = generate_caption(post.to_json(), full=False)
    buttons = post.generate_button()
    await bot.edit_message(
        entity=CHAT_ID,
        message=event.message_id,
        file=post.pic_name,
        text=capt,
        buttons=buttons
    )


@bot.on(events.CallbackQuery(pattern="hapus"))
async def handle(event: CallbackQuery.Event):
    await bot.delete_messages(entity=CHAT_ID, message_ids=event.message_id)


@bot.on(events.CallbackQuery(pattern=r"cek"))
async def handle(event: CallbackQuery.Event):
    await send_loop_msg()
