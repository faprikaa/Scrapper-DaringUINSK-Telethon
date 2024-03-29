import psutil
from telethon import events

from core.bot import bot
from komen.komen import send_komen
from util.config import CHAT_ID


@bot.on(events.NewMessage(pattern='/komen(?:\s|$)(.*)'))
async def handler(event):
    msg_value = str(event.pattern_match.group(1)).strip()
    split = msg_value.split(" ")
    post_id = split[0]
    komen_value = " ".join(split[1:])
    await send_komen(post_id, komen_value)

@bot.on(events.NewMessage(pattern='(?i)/*usage'))
async def handler(event):
    ram = psutil.virtual_memory()[2]
    cpu = psutil.cpu_percent(4)

    await bot.send_message(CHAT_ID, f"Total RAM yang terpakai sebesar : `{ram}%`\n Total CPU yang terpakai sebesar : `{cpu}%`")
# @bot.on(events.NewMessage(pattern='/list'))
# async def handler(event):
#     datas = load_saved_data()
#     msg = "Saved Data : \n"
#     for data in datas:
#         msg += f"`{data}`\n"
#     bot_msg = await bot.send_message(CHAT_ID, msg)
#     await asyncio.sleep(600)
#     await bot.delete_messages(CHAT_ID, bot_msg)
