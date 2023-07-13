from pyrogram import Client, filters
from AutoPost.database import Database 

db = Database()

@Client.on_message(filters.channel & filters.command("check_from_chat"))
async def check_from_chat(client, message):
    from_chat_id = str(message.chat.id)
    entry = db.get_chat_ids(from_chat_id)
    if entry:
        from_chat_id = entry["from_chat_id"] 
        to_chat_id = entry["to_chat_id"]
        await message.reply_text(f"Your 'from' chat ID: {from_chat_id}")
    else:
        await message.reply_text("You haven't set a forwarding connection.")
