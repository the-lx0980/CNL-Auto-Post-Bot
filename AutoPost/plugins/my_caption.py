import logging
import asyncio
from pyromod import listen
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
async def callback_handler(bot: Client, msg_query: CallbackQuery):
    query_data = msg_query.data
    user_id = msg_query.from_user.id
    
    if query_data == 'set_caption':
        answer = await message.chat.ask('*Send me your name:*', parse_mode=enums.ParseMode.MARKDOWN)
        await answer.request.edit_text("Name received!")
        await answer.reply(f'Your name is: {answer.text}', quote=True)    
        reply = answer.txt
        if reply:
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


# from pyromod import listen

@Client.on_message(filters.private & filters.command("test"))
async def snd_something(client, message):
    asking = await c.ask(chat_id, 'send something..')
    await message.reply_text(f"Your text: {asking.text}")
    
