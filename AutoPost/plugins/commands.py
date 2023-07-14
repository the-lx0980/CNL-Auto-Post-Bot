from pyrogram import Client, filters, enums
from AutoPost.database import Database 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

db = Database()

@Client.on_message(filters.channel & filters.command("check_from_chat"))
async def check_from_chat(client, message):
    channel_id = str(message.chat.id) 
    entry = db.get_channel_id(channel_id)
    """
    if entry:
        from_chat_id, to_chat_id = entry
        await message.reply_text(f"Your 'from' chat ID: {from_chat_id}\nTo Chat ID: {to_chat_id}")
    else:
        await message.reply_text("You haven't set a forwarding connection.")
    """

"""   
@Client.on_message(filters.private & filters.command('delete_connection'))  
async def delete_connection_command(client, message):
    user_id = str(message.from_user.id)
    command_parts = message.text.split(' ', 3)

    if len(command_parts) == 4:
        from_chat_id = command_parts[1]
        to_chat_id = command_parts[2]

        # Delete the connection
        db.delete_connection(user_id, from_chat_id, to_chat_id)

        reply_text = "Connection deleted successfully."
        await message.reply_text(reply_text)
    else:
        reply_text = 'Invalid command format. Please use /delete_connection {from_chat_id} {to_chat_id}'
        await message.reply_text(reply_text)
"""
@Client.on_message(filters.command('clear_database') & filters.user(5326801541))
async def clear_database_command(client, message):
    # Clear the entire database
    db.clear_database()
    reply_text = "Database cleared successfully."
    await message.reply_text(reply_text)
"""
@Client.on_message(filters.private & filters.command('add_block_text'))
async def add_block_text_command(client, message):
    user_id = str(message.from_user.id)
    command_parts = message.text.split(' ', 2)

    if len(command_parts) == 3:
        from_chat_id = command_parts[1]
        text = command_parts[2]

        # Add the block text
        db.add_block_text(user_id, from_chat_id, text)

        reply_text = f"Block text '{text}' added for chat ID '{from_chat_id}'."
        await message.reply_text(reply_text)
    else:
        reply_text = 'Invalid command format. Please use /add_block_text {from_chat_id} {text}'
        await message.reply_text(reply_text)

@Client.on_message(filters.private & filters.command('check_blocked_text'))
async def check_blocked_text_command(client, message):
    try:
        if len(message.text.split()) > 1:
            from_chat_id = str(message.text.split(' ', 1)[1])
            blocked_texts = db.get_texts(from_chat_id)

            if blocked_texts:
                reply_text = f"Blocked texts for channel ID <code>{from_chat_id}</code>:\n\n"
                for index, text in enumerate(blocked_texts, start=1):
                    reply_text += f"{index}. {text}\n"

                await message.reply_text(reply_text, parse_mode=enums.ParseMode.HTML) 
            else:
                await message.reply_text(f"No blocked texts found for channel ID <code>{from_chat_id}</code>.", parse_mode=enums.ParseMode.HTML)
        else:
            command_format = "/check_blocked_text <code>{channel_id}</code>"
            reply_text = f"Please provide a channel ID as an argument.\n\nCommand format: {command_format}"
            await message.reply_text(reply_text, parse_mode="HTML")
    except Exception as e:
        await message.reply_text(f"An error occurred: <code>{str(e)}</code>", parse_mode=enums.ParseMode.HTML)
"""

