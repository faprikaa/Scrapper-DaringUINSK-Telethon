import asyncio
import selenium
import time

from bot import bot
from core.browser import init_browser
from core.web import login


# from command_handler import *
# from scheduler import *
# from bot.button_callback_handler import *



async def main():
    browser = init_browser()
    await login(browser)
    # data = jsonf_read()
    # await init_schedul(data)
    print("bot berjalan")
    await bot.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())