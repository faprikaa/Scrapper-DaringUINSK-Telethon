import asyncio
from datetime import datetime

from telethon import Button

from core.bot import bot
from core.browser import browser
from core.web import cek_jenis_all
from util.config import SENIN, SELASA, RABU, JUMAT, TIMEZONE, CHAT_ID, LOOPING_SCHEDULER_INTERVAL

should_run = True
loop_msg = None  # Initialize loop_msg as a global variable
total_cek = 0


async def minute_check(time_ranges):
    global total_cek, should_run
    current_time = datetime.now(TIMEZONE).time()
    for time_range in time_ranges:
        start_time, end_time = map(lambda x: datetime.strptime(x, "%H:%M").time(), time_range.split(" - "))
        if start_time <= current_time < end_time:
            msg_start = await bot.send_message(CHAT_ID,
                                               f"Memasuki Mode Auto Cek\nMulai : {start_time}\nSelesai : {end_time}")
            total_cek = 0
            while datetime.now(TIMEZONE).time() < end_time and should_run:
                total_cek += 1
                await send_loop_msg()
                await asyncio.sleep(LOOPING_SCHEDULER_INTERVAL)
            should_run = False
            await bot.delete_messages(CHAT_ID, msg_start)
            msg_end = await bot.send_message(CHAT_ID,
                                             f"Mengakhiri Mode Auto Cek\nTotal Cek : {total_cek}\nSelesai : {end_time}")
            await bot.delete_messages(CHAT_ID, loop_msg)
            await asyncio.sleep(600)  # Wait for 10 minutes
            await bot.delete_messages(CHAT_ID, msg_end)


async def send_loop_msg():
    global loop_msg  # Declare loop_msg as global before using it
    browser.refresh()
    cek_result = await cek_jenis_all(force=False)
    last_check = datetime.now(TIMEZONE).time()
    total_new_ids = len(cek_result)
    if total_new_ids > 0:
        result = f"{total_new_ids} New Post"
    else:
        result = "Tidak ada post baru"
    msg = f"Sedang melakukan auto scrape\nLast Check = {last_check}\nResult = {result}\nTotal Cek = {total_cek}"

    if loop_msg:
        await bot.edit_message(
            entity=CHAT_ID,
            message=loop_msg.id,
            text=msg,
            buttons=[
                Button.inline('recheck', "cek")
            ]
        )
    else:
        loop_msg = await bot.send_message(CHAT_ID, msg, buttons=[
            Button.inline('recheck', "cek")
        ])


async def jadwal_check():
    current_day = datetime.now(TIMEZONE).strftime("%A")
    if current_day == "Monday":
        hari_arr = hari_parser(SENIN)
    elif current_day == "Tuesday":
        hari_arr = hari_parser(SELASA)
    elif current_day == "Wednesday":
        hari_arr = hari_parser(RABU)
    elif current_day == "Saturday":
        hari_arr = hari_parser(RABU)
    elif current_day == "Sunday":
        hari_arr = hari_parser(RABU)
    elif current_day == "Friday":
        hari_arr = hari_parser(JUMAT)
    else:
        return
    await minute_check(hari_arr)


def hari_parser(hari):
    try:
        hari_arr = hari.split(", ")
        return hari_arr
    except:
        print(Exception)


async def set_should_run(value: bool = False):
    global should_run
    should_run = value
    msg = await bot.send_message(CHAT_ID, "Berhasil stop Scheduler !\nAkan berhenti pada iterasi berikutnya")
    await asyncio.sleep(600)
    await bot.delete_messages(CHAT_ID, msg)