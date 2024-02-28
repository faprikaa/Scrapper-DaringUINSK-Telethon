from telethon import events
from telethon.events.callbackquery import CallbackQuery

from core.bot import bot
from core.classes.File import FileFromPost
from core.classes.Post import Post
from function.scheduler import send_loop_msg
from util.config import CHAT_ID
from utils import generate_caption


@bot.on(events.CallbackQuery(pattern=r"^download_file_\d+$"))
async def handle(event: CallbackQuery.Event):
    post_id = event.data.decode().removeprefix("download_file_")
    file = FileFromPost(post_id)
    if file.total_file != 0:
        await file.send_files(reply_msg_id=event.message_id)


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
    capt = generate_caption(post.to_json())
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
