import asyncio
import importlib
import os
import signal
import sys
from datetime import datetime

import croniter
import tornado.ioloop
import tornado.platform.asyncio
from pytz import timezone

import config
from config import BANNED_USERS, LOG_GROUP_ID
from ATMusic import HELPABLE, LOGGER, app, userbot
from ATMusic.core.call import AT
from ATMusic.plugins import ALL_MODULES
from ATMusic.utils.database import get_banned_users, get_gbanned


async def shutdown(loop):
    print("» AtrinMusicGirl Bot ..")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    print("» AtrinMusicGirl proses yang sedang berjalan ..")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("» Bot berhasil dihentikan.")


async def auto_restart():
    tz = timezone("Asia/tehran")
    cron = croniter.croniter("00 00 * * *", datetime.now(tz))
    while True:
        now = datetime.now(tz)
        next_run = cron.get_next(datetime)

        wait_time = (next_run - now).total_seconds()
        await asyncio.sleep(wait_time)
        await app.send_message(LOG_GROUP_ID, "<b>Restart Daily ..")
        # os.system("git pull --rebase -f")
        # os.system("pip3 install --no-cache-dir -U -r requirements.txt")
        os.execl(sys.executable, sys.executable, "-m", "ATMusic")


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER("ATMusic").error("No Assistant Clients Vars Defined!.. Exiting Process.")
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("ATMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module

    LOGGER("ATMusic.plugins").info("Successfully Imported All Modules ")
    await userbot.start()
    await AT.start()
    await AT.decorators()
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(loop)))
    LOGGER("ATMusic").info("AT Music Bot Started Successfully")
    await auto_restart()
    try:
        await stop_event.wait()
    except asyncio.CancelledError:
        pass
    finally:
        await app.stop()
        await userbot.stop()
        await Acdc.stop()
        await app2.stop()


if __name__ == "__main__":
    tornado.platform.asyncio.AsyncIOMainLoop().install()
    loop = tornado.ioloop.IOLoop.current().asyncio_loop
    try:
        loop.run_until_complete(init())
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown(loop))
