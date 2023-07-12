import logging
from AutoPost.database import Database
from AutoPost.user import UserBot as Bot
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

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
            from_chat_txt = await cb.message.reply_text("Send me your 'from' Channel ID starting with -100:")
            from_chat_id = (await client.listen(from_chat_txt)).text
            from_chat_id = from_chat_id.strip()

            if not from_chat_id.startswith("-100"):
                await cb.message.reply_text("Invalid 'from' Chat ID. Please start with -100.")
                await from_chat_txt.delete()
                return

            to_chat_txt = await cb.message.reply_text("Send me your 'to' Channel ID starting with -100:")
            to_chat_id = (await client.listen(to_chat_txt)).text
            to_chat_id = to_chat_id.strip()

            if not to_chat_id.startswith("-100"):
                await cb.message.reply_text("Invalid 'to' Chat ID. Please start with -100.")
                await from_chat_txt.delete()
                await to_chat_txt.delete()
                return

            await from_chat_txt.delete()
            await to_chat_txt.delete()
            
            added = db.add_forwarding(user_id, from_chat_id, to_chat_id)
            if added:
                await cb.message.reply_text(f"Forwarding set from `{from_chat_id}` to `{to_chat_id}`.")
            else:
                await cb.message.reply_text("You have already set forwarding for your channel IDs.")

        except Exception as e:
            logger.exception(e)
            await cb.message.reply_text(f"Error:\n{str(e)}")
