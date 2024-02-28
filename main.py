import asyncio

from core.bot import bot as Bot
from core.web import login
from bot import *
from komen.komen import cek_komen
from util.config import USE_SCHEDULER, LOOPING_INTERVAL


async def main():
    await login()
    # data = jsonf_read()
    # await init_schedul(data)
    print("bot berjalan")
    # print(cek_komen("217646"))
    if USE_SCHEDULER:
        from function.scheduler import jadwal_check
        while True:
            await jadwal_check()
            await asyncio.sleep(LOOPING_INTERVAL)
    await Bot.run_until_disconnected()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
