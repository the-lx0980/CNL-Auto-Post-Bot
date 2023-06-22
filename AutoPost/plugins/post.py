# (c) @TheLx0980
# Year : 2023

import logging
from pyrogram import Client, filters, enums

logger = logging.getLogger(__name__)
caption_position = "top".lower()

media_filter = filters.document | filters.video

@Client.on_message(filters.channel & (media_filter))
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

        # Remove username and link from caption
        file_caption = file_caption.replace("@MaxPlayHD", "").replace("👉", "")

        try:
            if caption_position == "top":
                await bot.copy_message(
                    chat_id=-1001986761426,
                    from_chat_id=-1001921917995,
                    message_id=update.id,
                    caption=file_caption + '\n\n' + f"**{caption_text}**",
                    parse_mode=enums.ParseMode.MARKDOWN
                )

        except:
            pass
