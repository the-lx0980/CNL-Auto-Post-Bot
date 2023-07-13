from AutoPost.database import Database
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

db = Database()


@Client.on_message(filters.command('my_channel'))
async def my_channel_command(client, message):
    try:
        user_id = str(message.from_user.id)
        channels = db.get_channels_for_user(user_id)
        if channels:
            buttons = []
            for channel in channels:
                from_chat_id = channel['from_chat_id']
                chat = await client.get_chat(int(from_chat_id))
                button = InlineKeyboardButton(chat.title, callback_data=f"managecl#{from_chat_id}")
                buttons.append([button])

            buttons.append([InlineKeyboardButton("Close", callback_data="close")])

            reply_markup = InlineKeyboardMarkup(buttons)
            reply_text = "Manage Your Channels:"  
            await client.send_message(chat_id=message.chat.id, text=reply_text, reply_markup=reply_markup)

        else:
            reply_text = "You have no channels."
            await client.send_message(chat_id=message.chat.id, text=reply_text)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await client.send_message(chat_id=message.chat.id, text=error_message)

