from AutoPost.database import Database
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

db = Database()

async def channels_pagination_callback(client, callback_query):
    try:
        user_id = str(callback_query.from_user.id)
        channels = db.get_channels_for_user(user_id)
        if channels:
            buttons = []
            start_index = int(callback_query.data.split('_')[1]) if '_' in callback_query.data else 0  # Extract the start index from the callback data
            channels_to_display = channels[start_index:start_index + 10]  # Get the next 10 channels

            for index, channel in enumerate(channels_to_display):
                from_chat_id = channel['from_chat_id']
                button = InlineKeyboardButton(str(from_chat_id), callback_data=f"managecl#{from_chat_id}")
                buttons.append([button])

            if start_index > 0:
                buttons.append([InlineKeyboardButton("Back", callback_data="prev_channels")])

            if start_index + 10 < len(channels):
                next_index = start_index + 10
                buttons.append([InlineKeyboardButton("Next", callback_data=f"next_channels_{next_index}")])
            else:
                buttons.append([InlineKeyboardButton("Back", callback_data="prev_channels")])

            reply_markup = InlineKeyboardMarkup(buttons)
            reply_text = "Your channels:"
            await client.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=reply_text, reply_markup=reply_markup)
        else:
            reply_text = "You have no channels."
            await client.send_message(chat_id=callback_query.message.chat.id, text=reply_text)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await client.send_message(chat_id=callback_query.message.chat.id, text=error_message)
