from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

CAPTION_DATA = {}

@Client.on_message(filters.private & filters.command("startt"))
async def start(bot, message):
    buttons = [
        [
            InlineKeyboardButton('Set Caption', callback_data='setcaption'),
            InlineKeyboardButton('Check Caption', callback_data='checkcaption')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply_text(
        text="Welcome! Click the buttons below to set or check the caption.",
        reply_markup=reply_markup
    )

@Client.on_callback_query()
async def callback_handler(bot, update):
    query_data = update.data
    user_id = update.from_user.id
    
    if query_data == 'setcaption':
        await bot.send_message(
            chat_id=user_id,
            text="Please send your desired caption within 30 seconds."
        )

        try:
            reply = await bot.listen(user_id, timeout=30)
        except asyncio.TimeoutError:
            await bot.send_message(
                chat_id=user_id,
                text="Caption not set. Timeout reached."
            )
        else:
            if reply.text:
                CAPTION_DATA[user_id] = reply.text
                await bot.send_message(
                    chat_id=user_id,
                    text="Caption set successfully."
                )
            else:
                await bot.send_message(
                    chat_id=user_id,
                    text="Invalid caption. Please try again."
                )
    
    elif query_data == 'checkcaption':
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

@Client.on_message(filters.text & filters.private)
async def handle_text_message(bot, message):
    user_id = message.from_user.id
    caption = CAPTION_DATA.get(user_id)
    if caption:
        await message.reply_text(text=message.text, caption=caption)
    else:
        await message.reply_text(text=message.text)
