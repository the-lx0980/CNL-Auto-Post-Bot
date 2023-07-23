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
        usr_me = await self.get_me()
        username = "Rentrox"
        if username:            
            await UserBot.send_message(self, chat_id=username, text="Hey bro Now AutoPost User Online")
        self.LOGGER(__name__).info(
            "User started!"
        )
        
    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
