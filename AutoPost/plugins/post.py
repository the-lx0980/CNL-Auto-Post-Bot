# (c) @TheLx0980
# Year : 2023

from AutoPost.helper_func import series_block
from pyrogram import Client, filters, enums
from AutoPost.database import Database 

db = Database()

@Client.on_message(filters.channel & (filters.document | filters.video))
async def editing(bot, message):
    channel_id = str(message.chat.id)
    get_data = db.get_caption(channel_id)
    replacing = db.get_replace_data(channel_id)
    if get_data:
        m_caption, from_chat_id = get_data
        if message.caption:
            media_caption = message.caption
            if any(block in media_caption for block in series_block):
                return
            if replacing:
                for data in replacing:
                    old_text = data['old_text']
                    new_text = data['new_text']
                    await bot.send_message(chat_id=int(channel_id), text=f"{old_text}\n{new_text}")
                    media_caption = media_caption.replace(old_text, new_text)
                    if "##" in media_caption:
                        media_caption = media_caption.replace("##", "")                                               
            caption = media_caption.strip()
            caption = f"**{caption}\n\n{m_caption}**"
            await bot.USER.copy_message(
                chat_id=-1001988988405,
                from_chat_id=int(from_chat_id),
                message_id=message.id,
                caption=caption,
                parse_mode=enums.ParseMode.MARKDOWN
            )
