import asyncio, selenium, time
from data_handler import *
from bot_handler import *
from broweb_handler import *
from command_handler import *
from scheduler import *
from selenium.common.exceptions import *

async def main():
    global browser, data, arr_id
    init_browser()
    browser = await login()
    init_bot_cmd(browser)
    arr_id = cek_id(browser)
    data = jsonf_read()
    # msg = await cek_jenis_all(browser, arr_id, data)
    # await send_msg(msg)
    await init_schedul(browser, data)
    await looping()
    await bot.run_until_disconnected()

async def looping():
    total_cek = 1   
    while True:
        try:
            await schedul()
            await asyncio.sleep(600)
            total_cek += 1
            send_total(total_cek)
        except :
            await send_msg(f"An error occured at looping, {traceback.format_exc()}")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
