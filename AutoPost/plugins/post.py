# (c) @TheLx0980
# Year : 2023

import logging
import asyncio
from AutoPost.helper_func import contains_blocked_text
from pyrogram import Client, filters, enums
from AutoPost.database import Database 

logger = logging.getLogger(__name__)
db = Database()

@Client.on_message(filters.channel & (filters.document | filters.video | filters.sticker))
async def editing(bot, message):
    channel_id = str(message.chat.id)
    get_data = db.get_caption(channel_id)
    replacing = db.get_replace_data(channel_id)
    forwardtag = db.get_forwardtag(channel_id) 
    if get_data:
        from_chat, to_chat, m_caption = get_data
        if message.caption:
            media_caption = message.caption
            if contains_blocked_text(media_caption, channel_id):
                return
            if replacing:
                for data in replacing:
                    old_text = data['old_text']
                    new_text = data['new_text']
                    media_caption = media_caption.replace(old_text, new_text)
                    if "##" in media_caption:
                        media_caption = media_caption.replace("##", "")
                        media_caption = ' '.join(media_caption.split())
            caption = media_caption.strip()
            if m_caption.strip() == '!()!':
                caption = f"**{caption}**"          
            else:
                caption = f"**{caption}\n\n{m_caption}**"
        if message.caption:
            caption = caption
        else:
            caption = message.caption
        try:
            if forwardtag:
                await bot.forward_messages(
                    chat_id=int(to_chat),
                    from_chat_id=int(from_chat),
                    message_ids=message.id
                )
            else:                
                await bot.copy_message(
                    chat_id=int(to_chat),
                    from_chat_id=int(from_chat),
                    message_id=message.id,
                    caption=caption,
                    parse_mode=enums.ParseMode.MARKDOWN
                )
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
