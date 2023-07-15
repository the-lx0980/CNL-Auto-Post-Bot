# (c) @TheLx0980
# Year : 2023

import logging
from . import API_ID, API_HASH, SESSION, LOGGER
from pyrogram import Client, __version__

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class UserBot(Client):
    def __init__(self):
        super().__init__(
            "userClient",
            api_hash=API_HASH,
            api_id=API_ID,
            session_string=SESSION,
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
