# (c) @TheLx0980
# Year : 2023

import logging
from . import API_ID, API_HASH, SESSION
from pyrogram import Client, __version__, enums

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
LOGGER = logging.getLogger("CNL-Auto-Post-Bot")

class UserBot(Client):
    def __init__(self):
        super().__init__(
            "userClient",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "AutoPost/plugins"},
            workers=20,
            bot_token=SESSION,
            sleep_threshold=10
        )
        self.LOGGER = LOGGER

    async def start(self, *args, **kwargs):
        # Handle extra args for run()
        await super().start(*args, **kwargs)
        bot_details = await self.get_me()
        self.set_parse_mode(enums.ParseMode.HTML)
        self.LOGGER.info(f"@{bot_details.username} started!")
    
    async def stop(self, *args, **kwargs):
        await super().stop(*args, **kwargs)
        self.LOGGER.info("Bot stopped. Bye.")
