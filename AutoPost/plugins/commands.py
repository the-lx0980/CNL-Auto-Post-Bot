# (c) Lx 0980
Hell = """
from AutoPost.Chat_msg import ChatMSG
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(client, message):
    await message.reply(
        text=ChatMSG.START_MSG,
        disable_web_page_preview=True,
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                InlineKeyboardButton("Help", callback_data="help"),
              #  InlineKeyboardButton("How Does This Works?", callback_data="abt")
            ]
        )
    )
"""



