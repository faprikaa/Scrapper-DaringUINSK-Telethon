import asyncio
import random
from datetime import datetime

from telethon import events, Button
from telethon.events import CallbackQuery

from core.bot import bot
from util.config import SENIN, SELASA, RABU, KAMIS, JUMAT, TIMEZONE, CHAT_ID

should_run = True
loop_msg = None  # Initialize loop_msg as a global variable
total_cek = 0


async def scheduler_check():
    skrg = datetime.now(TIMEZONE)
    current_day = skrg.strftime("%A")
    await jadwal_check(current_day)


async def minute_check(time_ranges):
    global total_cek
    current_time = datetime.now().time()
    for time_range in time_ranges:
        start_str, end_str = time_range.split(" - ")
        start_time = datetime.strptime(start_str, "%H:%M")
        end_time = datetime.strptime(end_str, "%H:%M")
        is_time_to_loop = start_time.time() <= current_time < end_time.time()
        if is_time_to_loop:
            await bot.send_message(CHAT_ID, "It's time to loop")
            await send_loop_msg()
            total_cek = 0
            while datetime.now().time() < end_time.time() and should_run:
                total_cek += 1
                await send_loop_msg()
                await asyncio.sleep(5)


def gen():
    return random.randint(1, 5)





async def send_loop_msg():
    global loop_msg  # Declare loop_msg as global before using it

    if loop_msg:
        await bot.edit_message(
            entity=CHAT_ID,
            message=loop_msg.id,
            text=gen_loop_msg(),
            buttons=[
                Button.inline('recheck', "cek")
            ]
        )
    else:
        loop_msg = await bot.send_message(CHAT_ID, gen_loop_msg(), buttons=[
            Button.inline('recheck', "cek")
        ])


def gen_loop_msg():
    last_check = datetime.now().time()
    result = gen()
    return f"""
Sedang melakukan auto scrape
Last Check = {last_check}
Result = {result}
Total Cek = {total_cek}
                    """


async def jadwal_check(hari):
    if hari == "Monday":
        today = SENIN
    elif hari == "Tuesday":
        today = SELASA
    elif hari == "Wednesday":
        today = RABU
    elif hari == "Saturday":
        today = RABU
    elif hari == "Sunday":
        today = RABU
    elif hari == "Thursday":
        today = KAMIS
    elif hari == "Friday":
        today = JUMAT
    else:
        return [" - ", "tidak ada jadwal"]
    hari_arr = hari_parser(today)
    await minute_check(hari_arr)


def hari_parser(hari):
    try:
        hari_arr = hari.split(", ")
        return hari_arr
    except:
        print(Exception)


@bot.on(events.NewMessage(pattern='/st'))
async def handler(event):
    asyncio.current_task().cancel()


async def main():
    await scheduler_check()
    await bot.run_until_disconnected()


asyncio.get_event_loop().run_until_complete(main())
