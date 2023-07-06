# (c) @TheLx0980
# Year : 2023
# Language : Python 3

import logging
from pyrogram import Client, idle
from pyromod import listen  # type: ignore
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid


logging.basicConfig(level=logging.INFO, encoding="utf-8", format="%(asctime)s - %(levelname)s - \033[32m%(pathname)s: \033[31m\033[1m%(message)s \033[0m")

app = Client(
    "Auto-Post-Bot",
    api_id=21288218,
    api_hash="dd47d5c4fbc31534aa764ef9918b3acd",
    bot_token="6285956621:AAHbImqbdlbHVd25xzuGydfsgz9GNTJclaE", 
    in_memory=True,
    plugins={'root':'AutoPost/plugins'},
)


if __name__ == "__main__":
    logging.info("Starting the bot")
    try:
        app.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    uname = app.me.username
    logging.info(f"@{uname} is now running!")
    idle()
    app.stop()
    logging.info("Bot stopped. Alvida!")

