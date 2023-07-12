# (c) @TheLx0980
# Year : 2023

import re
import logging
from AutoPost.helper_func import series_block, remove_content
from AutoPost.database import Database
from pyrogram import Client, filters, enums

logger = logging.getLogger(__name__)
db = Database()

@Client.on_message(filters.channel & (filters.document | filters.video))
async def editing(bot, message):
    from_chat_id = str(message.chat.id)
    forwarding = db.get_forwarding(from_chat_id)
    if forwarding:
        from_chat_id, to_chat_id = forwarding
        if message.document or message.video or message.audio:
            if message.caption:
                file_caption = f"**{message.caption}**"
            else:
                return  # Skip processing if no caption is present

            if any(block in file_caption for block in series_block):
                return

            text = file_caption
            file_caption = remove_content(text)

            caption = file_caption.strip()

            if caption:
                await bot.copy_message(
                    chat_id=int(to_chat_id),
                    from_chat_id=int(from_chat_id),
                    message_id=message.message_id,
                    caption=caption,
                    parse_mode=enums.ParseMode.MARKDOWN
                )



