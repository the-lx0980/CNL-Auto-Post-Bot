# (c) @TheLx0980
# Year : 2023

from AutoPost.helper_func import series_block
from pyrogram import Client, filters, enums

@Client.on_message(filters.channel & (filters.document | filters.video))
async def editing(bot, message):
    channel_id = str(message.chat.id)
    get_data = get_caption(channel_id)
    replaced = get_blocked(channel_id)
#
    if get_data:
        m_caption, from_chat_id = get_data
        if message.caption:
        else:
            return
        if blocked:   
            if any(block in media_caption for block in series_block):
                return
        text = media_caption
        file_caption = remove_content(text)
        caption = file_caption.strip()
        await bot.copy_message(
            chat_id=-1001547532818,
            from_chat_id=message.chat.id,
            message_id=message.id,
            caption=caption,
            parse_mode=enums.ParseMode.MARKDOWN
        )
