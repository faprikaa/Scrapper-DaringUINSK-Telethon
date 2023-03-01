import asyncio, time
from data_handler import *
from bot_handler import *
from broweb_handler import *
from scheduler import *

async def main():
    global brw, browser, bot, data, arr_id
    brw = init_browser()
    browser = await login(brw)
    arr_id = cek_id(browser)
    data = jsonf_read()
    bot = bot_prepare()
    msg = await cek_jenis_all(browser, arr_id, data)
    await send_msg(msg)
    await bot.run_until_disconnected()
    await looping()

async def looping():
    while True:
        schedul(brw, browser, data)
        asyncio.sleep(600)

@bot.on(events.NewMessage(pattern='(?i)/*cek'))
async def handler(event):
    await send_msg("Melakukan Cek")
    msg = await cek_jenis_all(browser, arr_id, data)
    await send_msg(msg)

@bot.on(events.NewMessage(pattern='(?i)/*fcek'))
async def handler(event):
    await send_msg("Melakukan Force Cek")
    await force_cek_jenis_all(browser, arr_id)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
