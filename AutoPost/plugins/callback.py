import logging
from asyncio.exceptions import TimeoutError
from pyromod import listen
from AutoPost.user import UserBot as Bot
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

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
    chat_id = cb.message.chat.id  
    if query_data == 'set_caption':
        try:
            channel_id = await client.ask(
                chat_id=chat_id,
                text="Send me your Channel ID with -100",
                timeout=300
            )
        except TimeoutError:
            return await cb.reply("You reached Time limit of 5 min.\nTry Again!")
        if channel_id.text:
            try:
                chat = await client.get_chat(int(channel_id.text))
            except Exception as e:
                print(e)
                return await cb.reply_text(f"Invalid Channel Id\n\n{e}")    
        if chat.id:
            try:
                caption = await client.ask(
                    chat_id=chat_id,
                    text="Send me your Channel Caption",
                    timeout=300
                )
            except TimeoutError:
                return await cb.reply("You reached Time limit of 5 min.\nTry Again!")
        if caption.text:
            channel_id = chat.id
            CAPTION_DATA[channel_id] = caption.text
            await cb.answer("Caption set successfully.")
        else:
            await cb.answer("Invalid caption. Please try again.")
    
    elif query_data == 'check_caption':
        channel_id = -1001547532818
        caption = CAPTION_DATA.get(channel_id)
        if caption:
            await client.send_message(
                chat_id=chat_id,
                text=f"Your saved caption is:\n{caption}"
            )
        else:
            await client.send_message(
                chat_id=chat_id,
                text="No caption found. Please set a caption first."
            )



