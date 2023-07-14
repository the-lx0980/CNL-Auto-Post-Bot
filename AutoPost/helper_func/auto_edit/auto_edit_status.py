from AutoPost.database import Database
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

db = Database()


async def set_channel(client, cb, query_data, _id):
    msg = cb.message
    channel_id = str(_id)
    auto_cap = db.
