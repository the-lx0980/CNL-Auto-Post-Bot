import logging
import asyncio
from pyromod import listen
from AutoPost import app as Bot
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
    user_id = cb.from_user.id
    
    if query_data == 'set_caption':
        answer = await client.chat.ask('Send me your name:', parse_mode=enums.ParseMode.MARKDOWN)
        await answer.request.edit_text("Name received!")
        await answer.reply(f'Your name is: {answer.text}', quote=True)
        reply = answer.text
        
        if reply:
            CAPTION_DATA[user_id] = reply
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



# from pyromod import listen

@Client.on_message(filters.private & filters.command("test"))
async def snd_something(client, message):
    answer = await message.chat.ask('*Send me your name:*', parse_mode=enums.ParseMode.MARKDOWN)
    await answer.request.edit_text("Name received!")
    await answer.reply(f'Your name is: {answer.text}', quote=True)    
