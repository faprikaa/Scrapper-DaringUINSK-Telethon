from telethon import events

from core.bot import bot
from core.web import cek_id, alert_checker, force_cek_jenis_all
from util.config import CHAT_ID
from util.web_utils import click_next


# @bot.on(events.NewMessage(pattern='/cek(?:\s|$)(.*)'))
# async def handler(event):
#     try:
#         cmd = int(event.pattern_match.group(1))
#
#         if cmd <= 5:
#             await bot.send_message(CHAT_ID, f"Melakukan {cmd} Cek")
#             arr_id = await cek_id()
#             arr_id2 = arr_id[0:cmd]
#             msg = await cek_jenis_all(arr_id2)
#             await send_msg(msg)
#     except:
#         cmd = event.pattern_match.group(1).strip().lower()
#         try:
#             if cmd == '':
#                 arr_id = await cek_id()
#                 await send_msg("Melakukan Cek")
#                 msg = await cek_jenis_all(arr_id)
#                 await send_msg(msg)
#             elif cmd == 'next':
#                 await send_msg("Melakukan Cek Next")
#                 next = click_next()
#                 arr_id = await cek_id()
#                 arr_id2 = arr_id[-5:]
#                 msg = await cek_jenis_all(arr_id2)
#                 await send_msg(msg)
#         except UnexpectedAlertPresentException:
#             await send_msg("Cookies habis, mengambil ulang")
#             await login()
#             msg = await cek_jenis_all(arr_id)
#             await send_msg(msg)
#         except:
#             await send_msg(f"An error occured at cek, {traceback.format_exc()}")


@bot.on(events.NewMessage(pattern='/fcek(?:\s|$)(.*)'))
async def handler(event):
    arr_id = await cek_id()
    argument = event.pattern_match.group(1).strip()
    msg = None

    if argument == "":
        alert_checker()
        msg = await bot.send_message(CHAT_ID, "Melakukan Force Cek")
        await force_cek_jenis_all(arr_id)
    elif argument == 'next':
        alert_checker()
        click_next()
        msg = await bot.send_message(CHAT_ID, "Melakukan Force Cek Next")
        arr_id = await cek_id()
        arr_id2 = arr_id[-5:]
        await force_cek_jenis_all(arr_id2)
    elif int(argument) >= 0:
        alert_checker()
        msg = await bot.send_message(CHAT_ID, f"Melakukan {argument} Force Cek ")
        arr_id = await cek_id()
        arr_id2 = arr_id[0:int(argument)]
        await force_cek_jenis_all(arr_id2)
    else:
        print(argument)
        print(type(argument))
    await bot.delete_messages(CHAT_ID, message_ids=msg.id)
