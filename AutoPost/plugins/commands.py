from pyrogram import Client, filters
from AutoPost.database import Database
from AutoPost import ADMINS 


db = Database()

@Client.on_message(filters.command("start"))
async def start(client, message):
    text = """
Welcome to AutoPost Bot!
This bot allows you to manage your channels and automate the process of forwarding messages with customized captions.
To get started, use the following commands:

• /add_channel - Add a channel to the database with a caption.
• /delete_channel - Delete a channel from the database.
• /add_replace_text - Add a replace text entry for a channel.
• /delete_replace_text - Delete a replace text entry for a channel.
• /delete_database - Delete database (Only admins)
Use these commands to set up and customize your channels for automated message forwarding
    """
    await message.reply_text(text)

    
@Client.on_message(filters.command("add_channel"))
async def add_channel_command(client, message):
    try:
        # Extract channel_id and caption from the command
        try:
            command_parts = message.text.split(" ", 2)
            caption = command_parts[2]
        except:
            command_parts = message.text.split(" ", 1)
            caption = None
            pass
            
        if len(command_parts) != 3:
            await message.reply_text("Invalid command format. Usage: /add_channel {channel_id} {caption}")
            return

        channel_id = command_parts[1]
        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID")
        # Add channel data to the database
        db.add_channel(str(channel_id), caption)
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
        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID,")
        old_text = command_parts[2]
        new_text = command_parts[3]

        db.save_replace_text(str(channel_id), old_text, new_text)
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


@Client.on_message(filters.private & filters.command("delete_database"))
async def delete_database_command(client, message):
    if str(message.chat.id) not in ADMINS:
        command_parts = message.text.split(" ", 1)
        if len(command_parts) != 2:
            await message.reply_text("Invalid command format. Usage: /delete_database {channel_id}")
            return
         
        channel_id = command_parts[1]
        
        delete = db.delete_all_replace_text(channel_id)
        await message.reply_text(f"Database deleted successfully!\nTotal Deleted: {delete}")
    else:
        await message.reply_text("You are not authorized to perform this command. or invalid ID")
        
        
