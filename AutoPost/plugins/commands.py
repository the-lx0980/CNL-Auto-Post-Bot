from pyrogram import Client, filters
from AutoPost.database import Database
from AutoPost import ADMINS 


db = Database()

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if str(message.chat.id) not in ADMINS:
        return await message.reply_text("This Bot is Not for Public")
    text = """
Welcome to AutoPost Bot!
This bot allows you to manage your channels and automate the process of forwarding messages with customized captions.
To get started, use the following commands:

• /add_channel - Add a channel to the database with a caption.
    format: (command) (from chat) (to_chat) (end text)
    if you don't want end text set caption = '!()!'
• /delete_channel - Delete a channel from the database.
    format: (command) (channel id)
• /add_replace_text - Add a replace text entry for a channel.
    format: (command) (channel id) || (old text) || (new text)
    seprate with '<code>||</code>'
• /delete_replace_text - Delete a replace text entry for a channel.
    format: (command) (channel id) (old text)
• /del_all_replace - Delete Replacing texts (Only bot admins)
    format: (command) (channel id)

Use these commands to set up and customize your channels for automated message forwarding
    """
    await message.reply_text(text)

    
@Client.on_message(filters.command("add_channel"))
async def add_channel_command(client, message):
    try:
        # Extract channel_id and caption from the command
        try:
            command_parts = message.text.split(" ", 3)
            caption = command_parts[3]
        except:
            command_parts = message.text.split(" ", 2)
            caption = None
            pass
            
        if len(command_parts) != 4:
            await message.reply_text("Invalid command format. Usage: /add_channel {channel_id} {caption}")
            return

        channel_id = command_parts[1]
        to_chat = command_parts[2]
        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID")
        # Add channel data to the database
        db.add_channel(str(channel_id), str(to_chat), caption)
        await message.reply_text(f"From Channel: {channel_id}\nTo Channel: {to_chat}\nCaption: {caption}\nadded successfully with successfully in Database")
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
        delete = db.delete_channel(channel_id)
        if delete:            
            await message.reply_text(f"Channel {delete} deleted successfully.")
        else:
            await message.reply_text("No Channel Found On Database")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Add Replace Text Command
@Client.on_message(filters.command("add_replace_text"))
async def add_replace_text_command(client, message):
    try:
        # Extract channel_id, old_text, and new_text from the command
        command_parts = message.text.split("||", 2)
        if len(command_parts) != 3:
            await message.reply_text("Invalid command format. Usage: /add_replace_text {channel_id} || {old_text} || {new_text}")
            return

        channel_id = command_parts[0].strip()
        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID.")
        old_text = command_parts[1].strip()
        new_text = command_parts[2].strip()

        db.save_replace_text(channel_id, old_text, new_text)
        await message.reply_text(f"<b>Old Text:</b> <code>{old_text}</code>\n<b>New Text:</b><code>{new_text}</code>\n\nReplace text added successfully.")
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


@Client.on_message(filters.private & filters.command("del_all_replace"))
async def delete_database_command(client, message):
    if str(message.chat.id) not in ADMINS:
        return
    command_parts = message.text.split(" ", 1)
    if len(command_parts) != 2:
        await message.reply_text("Invalid command format. Usage: /delete_database {channel_id}")
        return
         
    channel_id = command_parts[1]
        
    delete = db.delete_all_replace_text(channel_id)
    if delete:
        await message.reply_text(f"All replace text  deleted successfully!")
    else:
        await message.reply_text("You are not authorized to perform this command. or invalid ID")
    
        
        
        
