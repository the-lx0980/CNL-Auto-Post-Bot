from pyrogram import Client, filters
from AutoPost.database import Database 

db = Database()

@Client.on_message(filters.channel & filters.command("check_from_chat"))
async def check_from_chat(client, message):
    from_chat_id = str(message.chat.id)
    entry = db.get_chat_ids(from_chat_id)
    if entry:
        from_chat_id, to_chat_id = entry
        await message.reply_text(f"Your 'from' chat ID: {from_chat_id}\nTo Chat ID: {to_chat_id}")
    else:
        await message.reply_text("You haven't set a forwarding connection.")



@Client.on_message(filters.command('delete_connection'))
def delete_connection_command(client, message):
    chat_id = message.chat.id
    command_parts = message.text.split(' ', 3)

    if len(command_parts) == 4:
        from_chat_id = command_parts[1]
        to_chat_id = command_parts[2]

        # Delete the connection
        db.delete_connection(from_chat_id, to_chat_id)

        reply_text = "Connection deleted successfully."
        message.reply_text(reply_text)
    else:
        reply_text = 'Invalid command format. Please use /delete_connection {from_chat_id} {to_chat_id}'
        message.reply_text(reply_text)

@Client.on_message(filters.command('forward_list'))
def my_channel_command(client, message):
    user_id = str(message.chat.id)
    channels = db.get_channels_for_user(user_id)
    if channels:
        reply_text = ""
        for idx, channel in enumerate(channels, 1):
            from_chat_id = channel['from_chat_id']
            to_chat_id = channel['to_chat_id']
            reply_text += f"{idx}. From: {from_chat_id}\n   Target: {to_chat_id}\n\n"

        message.reply_text(reply_text)
    else:
        reply_text = "No channels found for the user."
        message.reply_text(reply_text)


@Client.on_message(filters.command('clear_database') & filters.user(ADMINS) 
def clear_database_command(client, message):
    # Clear the entire database
    db.clear_database()
    reply_text = "Database cleared successfully."
    message.reply_text(reply_text)
