from pyrogram import Client, filters
from AutoPost.database import Database

db = Database()

# Add Channel Command
@Client.on_message(filters.command("add_channel"))
async def add_channel_command(client, message):
    try:
        # Extract channel_id and caption from the command
        command_parts = message.text.split(" ", 2)
        if len(command_parts) != 3:
            await message.reply_text("Invalid command format. Usage: /add_channel {channel_id} {caption}")
            return

        channel_id = command_parts[1]
        caption = command_parts[2]

        # Add channel data to the database
        db.add_channel(channel_id, caption)
        await message.reply_text(f"Channel {channel_id} added successfully with caption: {caption}")
    except ValueError as e:
        await message.reply_text(str(e))
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Delete Channel Command
@Client.on_message(filters.command("delete_channel"))
async def delete_channel_command(client, message):
    try:
        # Extract channel_id from the command
        command_parts = message.text.split(" ", 1)
        if len(command_parts) != 2:
            await message.reply_text("Invalid command format. Usage: /delete_channel {channel_id}")
            return

        channel_id = command_parts[1]

        # Delete channel data from the database
        db.delete_channel(channel_id)
        await message.reply_text(f"Channel {channel_id} deleted successfully.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Add Replace Text Command
@Client.on_message(filters.command("add_replace_text"))
async def add_replace_text_command(client, message):
    try:
        # Extract channel_id, old_text, and new_text from the command
        command_parts = message.text.split(" ", 3)
        if len(command_parts) != 4:
            await message.reply_text("Invalid command format. Usage: /add_replace_text {channel_id} {old_text} {new_text}")
            return

        channel_id = command_parts[1]
        old_text = command_parts[2]
        new_text = command_parts[3]

        # Add replace text data to the database
        db.save_replace_text(channel_id, old_text, new_text)
        await message.reply_text("Replace text added successfully.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Delete Replace Text Command
@Client.on_message(filters.command("delete_replace_text"))
async def delete_replace_text_command(client, message):
    try:
        # Extract channel_id, old_text, and new_text from the command
        command_parts = message.text.split(" ", 3)
        if len(command_parts) != 4:
            await message.reply_text("Invalid command format. Usage: /delete_replace_text {channel_id} {old_text} {new_text}")
            return

        channel_id = command_parts[1]
        old_text = command_parts[2]
        new_text = command_parts[3]

        # Delete replace text data from the database
        db.delete_replace_text(channel_id, old_text, new_text)
        await message.reply_text("Replace text deleted successfully.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
