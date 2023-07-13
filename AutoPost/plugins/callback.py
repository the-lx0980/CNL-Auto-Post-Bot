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
    try:
        query_data = cb.data
        user_id = str(cb.message.chat.id)
        if query_data == 'set_forward':
            from_chat_id = await cb.message.chat.ask("Send me your 'from' Channel ID starting with -100:",
                                                     parse_mode=enums.ParseMode.HTML)
            from_chat_id = from_chat_id.text
            try:
                if not from_chat_id.startswith("-100"):
                    if len(from_chat_id) < 14:
                        return await cb.message.reply_text("Invalid Chat ID...\nChat ID should be something like this: <code>-100xxxxxxxxxx</code>")
            except Exception:
                return await cb.message.reply_text("Invalid Input...\nYou should specify a valid <code>chat_id (-100xxxxxxxxxx)</code>")
            from_chat_id = str(from_chat_id)

            to_chat_id = await cb.message.chat.ask("Send me your 'to' Channel ID starting with -100:",
                                                   parse_mode=enums.ParseMode.HTML)
            to_chat_id = str(to_chat_id.text)
            if to_chat_id:
                try:
                    if not to_chat_id.startswith("-100"):
                        if len(to_chat_id) < 14:
                            return await cb.message.reply_text("Invalid Chat ID...\nChat ID should be something like this: <code>-100xxxxxxxxxx</code>")
                except Exception:
                    return await cb.message.reply_text("Invalid Input...\nYou should specify a valid <code>chat_id (-100xxxxxxxxxx)</code>")

            await client.send_message(chat_id=cb.message.chat.id, text=f"User ID: {user_id}\nSource ID: {from_chat_id}\nTarget ID: {to_chat_id}")
            await db.save_chat_ids(user_id, from_chat_id, to_chat_id)
            get_data = db.get_chat_ids(from_chat_id)
            if get_data:
                from_chat_id, to_chat_id = get_data
                await cb.message.reply_text(f"Forwarding set from `{from_chat_id}` to `{to_chat_id}`.")
            else:
                await cb.message.reply_text("You have already set forwarding for your channel IDs.")
    except Exception as e:
        print("Error occurred in callback_handler:", str(e))


