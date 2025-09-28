from pyrogram import Client, filters
from pyrogram.types import Message
from AutoPost.database import Database
from AutoPost import ADMINS 


db = Database()

@Client.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if message.chat.id not in ADMINS:
        return await message.reply_text("This Bot is Not for Public")
    text = """
Welcome to AutoPost Bot!
This bot allows you to manage your channels and automate the process of forwarding messages with customized captions.
To get started, use the following commands:

• /add_channel - Add a channel to the database with a caption.
    <b>format:</b> <code>(command) (from chat) (to_chat) (end text)</code>
    <u>if you don't want end text set caption = <b>" !()! "</b></u>

• /delete_channel - Delete a channel from the database.
    <b>format:</b> <code>(command) (channel id)</code>


            <b>---> <u>For Replacing</u> <---</b>
            
• /add_replace_text - Add a replace text entry for a channel.
    <b>format:</b> <code>(command) (channel id) |:| (old text) |:| (new text)</code>   
    seprate with "<code>|:|</code>"

• /delete_replace_text - Delete a replace text entry for a channel.
    <b>format:</b> <code>(command) (channel id) (old text)</code>

• /del_all_replace - Delete Replacing texts (Only bot admins)
    <b>format:</b> <code>(command) (channel id)</code>


            <b>---> <u>For Blocking</u> <---</b>
            
• /save_blocked_text - add block text
    <b>format:</b> <code>(command) (channel id) (block text)</code>

• /get_blocklist - get list all blocked texts
    <b>format:</b> <code>(command) (channel id)</code>

• /del_block_text - Remove Blacklist Word
    <b>format:</b> <code>(command) (channel id) (block text)</code>

• /del_blocklist - Remove All Blacklist Words 
    <b>format:</b> <code>(command) (channel id)</code>

            <b>---> <u>Extra Commands</u> <---</b>
            
• /forwardtag - on or off 'Forwarded from' tag for a channel
    <b>format:</b> <code>(command) (channel id) (on/off)</code>

• /removealllinks - on/off remove all links in message caption
    <b>format:</b> <code>(command) (channel id) (on/off)</code>
    
            <b>---> <u>For Database</u> <---</b>
• /cleardb - Delete all info from database 
    """
    await message.reply_text(text)

    
@Client.on_message(filters.command("add_channel") & filters.user(ADMINS))
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
            await message.reply_text("Invalid command format. Usage: /add_channel (from_chat_id) (to_chat_id) (end caption}")
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
@Client.on_message(filters.command("delete_channel") & filters.user(ADMINS))
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
@Client.on_message(filters.command("add_replace_text") & filters.user(ADMINS))
async def add_replace_text_command(client, message):
    try:
        # Extract channel_id, old_text, and new_text from the command
        command_parts = message.text.split("|:|", 2)
        
        replace = command_parts[0].replace("/add_replace_text", "")
        channel_id = replace.strip()
        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID.")
        old_text = command_parts[1].strip()
        new_text = command_parts[2].strip()
      #  await message.reply_text(f"{channel_id}\n{old_text}\n{new_text}")
        db.save_replace_text(channel_id, old_text, new_text)
        await message.reply_text(f"<b>Old Text:</b> <code>{old_text}</code>\n<b>New Text:</b> <code>{new_text}</code>\n\nReplace text added successfully.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

# Delete Replace Text Command
@Client.on_message(filters.command("delete_replace_text") & filters.user(ADMINS))
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


@Client.on_message(filters.command("del_all_replace") & filters.user(ADMINS))
async def delete_database_command(client, message):
    command_parts = message.text.split(" ", 1)
    if len(command_parts) != 2:
        await message.reply_text("Invalid command format. Usage: /delete_database {channel_id}")
        return
         
    channel_id = command_parts[1]
        
    delete = db.delete_all_replace_text(channel_id)
    if delete:
        await message.reply_text(f"All replace text  deleted successfully!")
    else:
        await message.reply_text("Replace Text Not found")
    



@Client.on_message(filters.command("save_blocked_text") & filters.user(ADMINS)) 
async def save_blocked_text_command(client, message):
    try:
        # Extract channel_id and text from the command
        command_parts = message.text.split(" ", 2)
        if len(command_parts) != 3:
            await message.reply_text("Invalid command format. Usage:\n\n<code>/save_block_text (channel_id) (text)</code>")
            return

        channel_id = command_parts[1].strip()
        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID.")

        text = command_parts[2].strip()

        saved = db.save_blocked_text(channel_id, text)
        if saved:
            await message.reply_text("Blocked text saved successfully.")
        else:
            await message.reply_text("Blocked text already exists for the channel.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("get_blocklist") & filters.user(ADMINS))
async def get_all_blocked_texts_command(client, message):
    try:
        # Extract channel_id from the command
        command_parts = message.text.split(" ", 1)
        if len(command_parts) != 2:
            await message.reply_text(
            """
            Invalid command format. Usage: 

            Example:
                <code>/get_blocklist (channel_id)"</code>
            """
            )
            return

        channel_id = command_parts[1].strip()
        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID.")

        blocked_texts = db.get_all_blocked_texts(channel_id)
        if blocked_texts:
            response = "\n".join(blocked_texts)
            await message.reply_text(f"Blocked texts for the channel:\n{response}")
        else:
            await message.reply_text("No blocked texts found for the channel.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("del_block_text") & filters.user(ADMINS))
async def delete_blocked_text_command(client, message):
    try:
        # Extract channel_id and text from the command
        command_parts = message.text.split(" ", 2)
        if len(command_parts) != 3:
            await message.reply_text("Invalid command format. Usage: <code>/del_block_text (channel_id) (text)<code>")
            return

        channel_id = command_parts[1].strip()
        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID.")

        text = command_parts[2].strip()

        deleted = db.delete_blocked_text(channel_id, text)
        if deleted:
            await message.reply_text("Blocked text deleted successfully.")
        else:
            await message.reply_text("Blocked text not found for the channel.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("del_blocklist") & filters.user(ADMINS))
async def delete_all_blocked_texts_command(client, message):
    try:
        command_parts = message.text.split(" ", 1)
        if len(command_parts) != 2:
            await message.reply_text("Invalid command format. Usage:\n\n<code>/del_blocklist (channel_id)</code>")
            return

        channel_id = command_parts[1].strip()
        if not channel_id.startswith("-100"):
            await message.reply_text("Invalid Channel ID.")
            return

        deleted_count = db.delete_all_blocked_texts(channel_id)
        await message.reply_text(f"All blocked texts deleted for channel {channel_id}. Total deleted: {deleted_count}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_message(filters.command("forwardtag") & filters.user(ADMINS))
async def forwardtag_command(client, message: Message):
    """
    Usage: /forwardtag <channel_id> on/off
    Example: /forwardtag -1001234567890 on
    """
    try:
        command_parts = message.text.split(" ", 2)
        if len(command_parts) != 3:
            return await message.reply_text(
                "Invalid format.\n\nUsage:\n<code>/forwardtag (channel_id) on/off</code>"
            )

        channel_id = command_parts[1].strip()
        option = command_parts[2].strip().lower()

        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID. Must start with <code>-100</code>.")

        if option not in ["on", "off"]:
            return await message.reply_text("Invalid option. Use <code>on</code> or <code>off</code>.")

        value = True if option == "on" else False
        updated = db.set_forwardtag(channel_id, value)

        if updated:
            await message.reply_text(
                f"✅ Forward tag for <code>{channel_id}</code> set to <b>{'ON' if value else 'OFF'}</b>"
            )
        else:
            await message.reply_text(
                "⚠️ Channel not found in DB. Please add it first using /add_channel."
            )

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
        
@Client.on_message(filters.command("removealllinks") & filters.user(ADMINS))
async def removealllinks_command(client, message: Message):
    """
    Usage: /removealllinks <channel_id> on/off
    Example: /removealllinks -1001234567890 on
    """
    try:
        command_parts = message.text.split(" ", 2)
        if len(command_parts) != 3:
            return await message.reply_text(
                "Invalid format.\n\nUsage:\n<code>/removealllinks (channel_id) on/off</code>"
            )

        channel_id = command_parts[1].strip()
        option = command_parts[2].strip().lower()

        if not channel_id.startswith("-100"):
            return await message.reply_text("Invalid Channel ID. Must start with <code>-100</code>.")

        if option not in ["on", "off"]:
            return await message.reply_text("Invalid option. Use <code>on</code> or <code>off</code>.")

        value = True if option == "on" else False
        updated = db.set_hidden_links(channel_id, value)

        if updated:
            await message.reply_text(
                f"✅ Forward tag for <code>{channel_id}</code> set to <b>{'ON' if value else 'OFF'}</b>"
            )
        else:
            await message.reply_text(
                "⚠️ Channel not found in DB. Please add it first using /add_channel."
            )

    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
                
@Client.on_message(filters.command("cleardb") & filters.user(ADMINS))
async def del_db(client, message):
    try:
        delete = db.cleardb()
        await message.reply_text(f"Database Successfully Deleted\n<b>Total Deleted:</b> {delete}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
