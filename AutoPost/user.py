# (c) @TheLx0980
# Year : 2023

from . import Info, LOGGER
from pyrogram import Client, __version__

class Userbot(Client, Info):
    def __init__(self):
        super().__init__(
            "userClient",
            api_hash=self.API_HASH,
            api_id=self.API_ID,
            bot_token=self.SESSION,
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
