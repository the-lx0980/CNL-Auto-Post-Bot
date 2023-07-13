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



get_channels_for_user

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
