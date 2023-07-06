import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import MessageNotModified

logger = logging.getLogger(__name__)

CAPTION_DATA = {}

@Client.on_message(filters.private & filters.command("start"))
async def start(bot, message):
    buttons = [
        [
            InlineKeyboardButton('Set Caption', callback_data='set_caption'),
            InlineKeyboardButton('Check Caption', callback_data='check_caption')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text="Welcome! Click the buttons below to set or check the caption.",
        reply_markup=reply_markup
    )

@Client.on_callback_query()
async def callback_handler(bot: Client, msg_query: CallbackQuery):
    query_data = msg_query.data
    user_id = msg_query.from_user.id
    
    if query_data == 'set_caption':
        reply = await bot.ask(user_id, 'Please send your `caption`', filters=filters.text)         
        if reply.text:
            CAPTION_DATA[user_id] = reply.text
            await msg_query.answer("Caption set successfully.")
        else:
            await msg_query.answer("Invalid caption. Please try again.")

    elif query_data == 'check_caption':
        caption = CAPTION_DATA.get(user_id)
        if caption:
            await bot.send_message(
                chat_id=user_id,
                text=f"Your saved caption is:\n{caption}"
            )
        else:
            await bot.send_message(
                chat_id=user_id,
                text="No caption found. Please set a caption first."
            )
