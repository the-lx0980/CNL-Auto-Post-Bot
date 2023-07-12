# (c) @TheLx0980
# Year : 2023

import re
from .callback import CAPTION_DATA
import logging
from AutoPost.helper_func import series_block
from AutoPost.database import Database
from pyrogram import Client, filters, enums

logger = logging.getLogger(__name__)
caption_position = "top".lower()

media_filter = filters.document | filters.video

db = Database()

@Client.on_message(filters.channel & media_filter)
async def editing(bot, message):

    try:
        media = message.document or message.video or message.audio
        caption_text = "@HQFilms4u"
    except:
        caption_text = ""
        pass

    if message.document or message.video or message.audio:
        if message.caption:
            file_caption = f"**{message.caption}**"
        else:
            fname = media.file_name
            filename = fname.replace("_", ".")
            file_caption = f"`{filename}`"

        if any(block in file_caption for block in series_block):
            return

        text = file_caption
        file_caption = remove_content(text)
        
        try:
            await bot.copy_message(
                chat_id=to_chat_id,
                from_chat_id=from_chat_id,
                message_id=message.message_id,
                caption=caption,
                parse_mode=enums.ParseMode.MARKDOWN
            )
        except:
            pass

def remove_content(text):
    # Remove username and link
    text = text.replace("@MaxPlayHD", "").replace("👉", "")
    # Remove additional text
    text = text.replace("Join Us On Telegram", "").replace("Support us", "").replace("🙏", "").replace("❤️", "")
    return text
