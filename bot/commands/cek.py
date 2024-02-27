from telethon import events

from core.bot import bot
from core.web import cek_id, alert_checker, cek_jenis_all, click_next
from util.config import CHAT_ID


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
        await cek_jenis_all(arr_id, False)
    elif argument == 'next':
        alert_checker()
        await click_next()
        msg = await bot.send_message(CHAT_ID, "Melakukan Force Cek Next")
        arr_id = await cek_id()
        arr_id2 = arr_id[-5:]
        await cek_jenis_all(arr_id2, False)
    elif int(argument) >= 0:
        alert_checker()
        msg = await bot.send_message(CHAT_ID, f"Melakukan {argument} Force Cek ")
        arr_id = await cek_id()
        arr_id2 = arr_id[0:int(argument)]
        await cek_jenis_all(arr_id2, False)
    else:
        print(argument)
        print(type(argument))
    await bot.delete_messages(CHAT_ID, message_ids=msg.id)


@bot.on(events.NewMessage(pattern='/cek(?:\s|$)(.*)'))
async def handler(event):
    arr_id = await cek_id()
    argument = event.pattern_match.group(1).strip()
    msg = None

    if argument == "":
        alert_checker()
        msg = await bot.send_message(CHAT_ID, "Melakukan Cek")
        await cek_jenis_all(arr_id, True)
    elif argument == 'next':
        alert_checker()
        await click_next()
        msg = await bot.send_message(CHAT_ID, "Melakukan Cek Next")
        arr_id = await cek_id()
        arr_id2 = arr_id[-5:]
        await cek_jenis_all(arr_id2, True)
    elif int(argument) >= 0:
        alert_checker()
        msg = await bot.send_message(CHAT_ID, f"Melakukan {argument} Cek ")
        arr_id = await cek_id()
        arr_id2 = arr_id[0:int(argument)]
        await cek_jenis_all(arr_id2, True)
    else:
        print(argument)
        print(type(argument))
    await bot.delete_messages(CHAT_ID, message_ids=msg.id)


@bot.on(events.NewMessage(pattern='/next'))
async def handler(event):
    await bot.send_message(CHAT_ID,await click_next())
