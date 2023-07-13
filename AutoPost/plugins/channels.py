from AutoPost.database import Database
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

db = Database()

@Client.on_callback_query(filters.regex('mychannel'))  
async def callback_handler(client, callback_query):
    chat_id = callback_query.message.chat.id
    from_chat_id = callback_query.data
    block_texts = db.get_texts(from_chat_id)
 
    if block_texts:
        reply_text = "Block texts:\n\n"
        for text in block_texts:
            reply_text += f"- {text}\n"

        await client.send_message(chat_id=chat_id, text=reply_text)
    else:
        reply_text = "No block texts found for this channel."
        await client.send_message(chat_id=chat_id, text=reply_text)


@Client.on_message(filters.command('my_channel'))
async def my_channel_command(client, message):
    user_id = str(message.from_user.id)
    channels = db.get_channels_for_user(user_id)
    if channels:
        buttons = []
        for channel in channels:
            from_chat_id = channel['from_chat_id']
            button = InlineKeyboardButton(str(from_chat_id), callback_data='mychannel_' + from_chat_id)
            buttons.append([button])

        reply_markup = InlineKeyboardMarkup(buttons)
        reply_text = "Your channels:"
        await client.send_message(chat_id=message.chat.id, text=reply_text, reply_markup=reply_markup)
    else:
        reply_text = "You have no channels."
        await client.send_message(chat_id=message.chat.id, text=reply_text)