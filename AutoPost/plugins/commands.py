from pyrogram import Client, filters
from AutoPost.database import Database 

db = Database()

@Client.on_message(filters.private & filters.command("check_from_chat"))
async def check_from_chat(client, message):
    from_chat_id = str(message.chat.id)
    entry = db.get_from_chat(from_chat_id)
    if entry:
        from_chat_id, to_chat_id = entry
        await message.reply_text(f"Your 'from' chat ID: {from_chat_id}")
    else:
        await message.reply_text("You haven't set a forwarding connection.")
