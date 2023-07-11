import logging
import asyncio
from pyromod import listen
from AutoPost.user import UserBot as Bot
from pyrogram import Client, filters, enums
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
async def callback_handler(client: Bot, cb: CallbackQuery):
    query_data = cb.data
    channel_id = cb.from_user.id
    
    if query_data == 'set_caption':
        try:
            caption = await cb.ask(
                chat_id= cb.chat.id,
                text="Send me your name",
                timeout=300
            )
        except TimeoutError:
            return await cb.reply("You reached Time limit of 5 min.\nTry Again!")
        caption = caption.text    
        if caption:
            CAPTION_DATA[channel_id] = caption
            await cb.answer("Caption set successfully.")
        else:
            await cb.answer("Invalid caption. Please try again.")

    elif query_data == 'check_caption':
        caption = CAPTION_DATA.get(user_id)
        if caption:
            await client.send_message(
                chat_id=user_id,
                text=f"Your saved caption is:\n{caption}"
            )
        else:
            await client.send_message(
                chat_id=user_id,
                text="No caption found. Please set a caption first."
            )



