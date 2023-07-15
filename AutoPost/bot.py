# (c) Lx 0980
# Year : 2023

import logging
from . import API_ID, API_HASH, BOT_TOKEN, LOGGER
from pyrogram import Client, __version__
from .user import UserBot as User

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

class UserBot(Client):
    USER: User = None
    USER_ID: int = None

    def __init__(self):
        super().__init__(
            "forward",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={
                "root": "AutoPost/plugins"
            },
            workers=200,
            bot_token=BOT_TOKEN,
            sleep_threshold=10
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        bot_details = await self.get_me()
        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER(__name__).info(
            f"@{bot_details.username}  started! "
        )
        self.USER, self.USER_ID = await User().start()

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped. Bye.")
