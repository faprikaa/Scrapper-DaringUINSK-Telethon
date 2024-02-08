import asyncio
import selenium
import time
from data_handler import *
from bot_handler import *
from broweb_handler import *
from command_handler import *
from scheduler import *
from selenium.common.exceptions import *


async def main():
    global browser, data
    browser = await login()
    data = jsonf_read()
    await init_schedul(data)
    print("bot berjalan")
    await looping()
    await bot.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
