from telethon import events

from core.bot import bot
from core.web import alert_checker, cek_jenis_all, click_next, get_html_ids
from function.scheduler import set_should_run
from util.config import CHAT_ID


@bot.on(events.NewMessage(pattern='/fcek(?:\s|$)(.*)'))
async def handler(event):
    argument = event.pattern_match.group(1).strip()
    msg = None
    alert_checker()

    if argument == "":
        msg = await bot.send_message(CHAT_ID, "Melakukan Force Cek")
        arr_id = await get_html_ids()
        await cek_jenis_all(arr_id, True)
    elif argument == 'next':
        await click_next()
        msg = await bot.send_message(CHAT_ID, "Melakukan Force Cek Next")
        arr_id = await get_html_ids()
        arr_id2 = arr_id[-5:]
        await cek_jenis_all(arr_id2, True)
    elif int(argument) >= 0:
        msg = await bot.send_message(CHAT_ID, f"Melakukan {argument} Force Cek ")
        arr_id = await get_html_ids()
        arr_id2 = arr_id[0:int(argument)]
        await cek_jenis_all(arr_id2, True)
    else:
        print(argument)
        print(type(argument))
    await bot.delete_messages(CHAT_ID, message_ids=msg.id)


@bot.on(events.NewMessage(pattern='/cek(?:\s|$)(.*)'))
async def handler(event):
    argument = event.pattern_match.group(1).strip()
    msg = None
    cek_result = None
    if argument == "":
        alert_checker()
        arr_id = await get_html_ids()
        msg = await bot.send_message(CHAT_ID, "Melakukan Cek")
        await cek_jenis_all(arr_id, False)
    elif argument == 'next':
        alert_checker()
        await click_next()
        msg = await bot.send_message(CHAT_ID, "Melakukan Cek Next")
        arr_id = await get_html_ids()
        arr_id2 = arr_id[-5:]
        await cek_jenis_all(arr_id2, False)
    elif int(argument) >= 0:
        alert_checker()
        msg = await bot.send_message(CHAT_ID, f"Melakukan {argument} Cek ")
        arr_id = await get_html_ids()
        arr_id2 = arr_id[0:int(argument)]
        await cek_jenis_all(arr_id2, False)
    else:
        print(argument)
        print(type(argument))
    await bot.edit_message(CHAT_ID, message=msg, text="Tidak ada postingan baru")


@bot.on(events.NewMessage(pattern='/next'))
async def handler(event):
    await bot.send_message(CHAT_ID, await click_next())


@bot.on(events.NewMessage(pattern='/stop'))
async def handler(event):
    await set_should_run(False)
