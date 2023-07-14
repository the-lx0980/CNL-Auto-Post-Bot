import logging
from AutoPost.database import Database
from AutoPost.user import UserBot as Bot
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

logger = logging.getLogger(__name__)
db = Database()



@Client.on_callback_query()
async def callback_handler(client: Bot, cb: CallbackQuery):
  query_data = cb.data
  user_id = str(cb.message.chat.id)
  await set_channel(client, cb, query_data, user_id)



async def set_channel(client, cb, query_data, user_id):
    if query_data == 'set_forward':
        channel_id = await cb.message.chat.ask("Send me your 'from' Channel ID starting with -100:", parse_mode=enums.ParseMode.HTML)
        channel_id = channel_id.text.strip()
        
        if not channel_id.startswith("-100"):
            return await cb.message.reply_text("Invalid Channel ID. Please enter a valid Channel ID With '-100'")
        
        if len(channel_id) > 14:
            return await cb.message.reply_text("Invalid Chat ID...\nChat ID should be something like this: <code>-100xxxxxxxxxx</code>")
        
        try:
            chat = await client.get_chat(int(channel_id))
            if chat.type != enums.ChatType.CHANNEL:
                return await cb.message.reply_text("This is not a valid channel ID. Please provide a channel ID.")
            if not await client.get_chat_member(chat.id, "me"):
                return await cb.message.reply_text("I am not an admin in the specified channel. Please make sure I am added as an admin.")
        except Exception as e:
            return await cb.message.reply_text(f"An error occurred while validating the channel ID: {str(e)}")
        
        channel_id = str(chat.id)
        db.save_channel_id(user_id, channel_id)
        get_data = db.get_channel_id(channel_id)
        if get_data:
            await cb.message.reply_text(f"{get_data} Channel successfully added. You can now manage your channel from the bot's private messages.")
        else:
            await cb.message.reply_text("You have already added this channel."
