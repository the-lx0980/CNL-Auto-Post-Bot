# (c) @TheLx0980
# Year : 2023

import logging
from pyromod import listen
from . import API_ID, API_HASH, SESSION, LOGGER
from pyrogram import Client, __version__

logging.basicConfig(level=logging.INFO, encoding="utf-8", format="%(asctime)s - %(levelname)s - \033[32m%(pathname)s: \033[31m\033[1m%(message)s \033[0m")


class UserBot(Client):
    def __init__(self):
        super().__init__(
            "userClient",
            api_hash=API_HASH,
            api_id=API_ID,
            bot_token=SESSION,
            workers=20,
            plugins={
                "root": "AutoPost/plugins"
            }
        )

        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        return (self, usr_bot_me.id)

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
