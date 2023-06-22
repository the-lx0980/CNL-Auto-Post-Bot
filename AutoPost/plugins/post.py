# (c) @TheLx0980
# Year : 2023

import logging
from pyrogram import Client, filters, enums

logger = logging.getLogger(__name__)
caption_position = "top".lower()

@Client.on_message(filters.channel & (media_filter))
async def editing(bot, message):
      try:
         media = message.document or message.video or message.audio
         caption_text = "@HQFilms4u"
      except:
         caption_text = ""
         pass 
      if (message.document or message.video or message.audio): 
          if message.caption:                        
             file_caption = f"**{message.caption}**"                
          else:
             fname = media.file_name
             filename = fname.replace("_", ".")
             file_caption = f"`{filename}`"  
              
      try:
          if caption_position == "top":
             await bot.edit_message_caption(
                 chat_id=message.chat.id, 
                 message_id=message.id,
                 caption=file_caption + "\n" + caption_text,
                 parse_mode=enums.ParseMode.MARKDOWN
             )

      except:
          pass
