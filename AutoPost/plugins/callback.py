import logging
from AutoPost.database import Database 
from AutoPost.user import UserBot as Bot
from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery 
from pyrogram.errors import BadRequest

logger = logging.getLogger(__name__)
db = Database()

@Client.on_message(filters.private & filters.command("start"))
async def start(bot, message):
    buttons = [
        [
            InlineKeyboardButton('Set Forward', callback_data='set_forward')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text="Welcome! Click the buttons below to set or check the caption.",
        reply_markup=reply_markup
    )

@Client.on_callback_query()
async def callback_handler(client: Bot, cb: CallbackQuery):
    query_data = cb.data   
    user_id = str(cb.message.chat.id) 
    if query_data == 'set_forward':
        try:
            from_chat_txt = await cb.message.chat.ask("Send me your from Channel ID with -100",
                                                     parse_mode=enums.ParseMode.HTML)       
        except Exception as e:
            logger.exception(e) 
            return await cb.message.reply_text(f"Error\n {e}")
        from_chat_id = from_chat_txt.text
        try:
            if not target_chat[0:4].startswith("-100"):
                if len(target_chat) < 14:
                    return await update.reply_text("Invalid Chat Id...\nChat ID Should Be Something Like This: <code>-100xxxxxxxxxx</code>")
        except Exception:
            return await update.reply_text("Invalid Input...\nYou Should Specify Valid <code>chat_id(-100xxxxxxxxxx)</code>>")
        from_chat_id = str(from_chat_id)   
        to_chat_id = await cb.message.chat.ask("Send Me Your Target Channel ID With '-100'",         
                                               parse_mode=enums.ParseMode.HTML)
        to_chat_id = str(to_chat_id.text)
        if to_chat_id:
            try:
                if not to_chat_id[0:4].startswith("-100"):
                    if len(to_chat_id) < 14:
                        return await update.reply_text("Invalid Chat Id...\nChat ID Should Be Something Like This: <code>-100xxxxxxxxxx</code>")
            except Exception:
                return await update.reply_text("Invalid Input...\nYou Should Specify Valid <code>chat_id(-100xxxxxxxxxx)</code>>")
        added = db.add_forwarding(user_id, from_chat_id, to_chat_id)
        if added:
            await cb.message.reply(f"Forwarding set from `{from_chat_id}` to `{to_chat_id}`.")
        else:
            await cb.message.reply("You have already set forwarding for your channel IDs.")

        
        
        
        
        
