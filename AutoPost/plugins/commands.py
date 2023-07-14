from pyrogram import Client, filters
from AutoPost.database import Database 

db = Database()


@Client.on_message(filters.command("add_replace_text"))
async def add_replace_text_command(_, message: Message):
    try:
        # Parse the command arguments
        args = message.text.split()[1:]
        if len(args) != 3:
            await message.reply_text("Invalid command format. Usage: /add_replace_text {channel_id} {old_text} {new_text}")
            return

        channel_id = args[0]
        old_text = args[1]
        new_text = args[2]

        # Save the replace text data to the database
        db.save_replace_text(channel_id, old_text, new_text)

        await message.reply_text("Replace text added successfully.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


@Client.on_message(filters.command("delete_replace_text"))
async def delete_replace_text_command(_, message: Message):
    try:
        # Parse the command arguments
        args = message.text.split()[1:]
        if len(args) != 3:
            await message.reply_text("Invalid command format. Usage: /delete_replace_text {channel_id} {old_text} {new_text}")
            return

        channel_id = args[0]
        old_text = args[1]
        new_text = args[2]

        # Delete the replace text data from the database
        db.delete_replace_text(channel_id, old_text, new_text)

        await message.reply_text("Replace text deleted successfully.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


@Client.on_message(filters.command("delete_all_replace_text"))
async def delete_all_replace_text_command(_, message: Message):
    try:
        # Parse the command argument
        channel_id = message.text.split()[1]

        # Delete all replace text data for the channel from the database
        db.delete_all_replace_text(channel_id)

        await message.reply_text("All replace text entries deleted successfully.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")
