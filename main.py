import asyncio

from core.bot import bot as Bot
from core.web import login
from bot.commands import *


async def main():
    await login()
    # data = jsonf_read()
    # await init_schedul(data)
    print("bot berjalan")
    await Bot.run_until_disconnected()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())