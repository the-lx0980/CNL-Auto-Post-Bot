# (c) Lx 0980

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters, enums

CAPTION_DATA = {}

@Client.on_callback_query()
async def callback_data(bot, update: CallbackQuery):
    query_data = update.data
    user_id = update.from_user.id
    
    if query_data == "start":
        buttons = [[            
            InlineKeyboardButton('मदद ⚙', callback_data="help")
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            f"Welcome {update.from_user.mention}",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
    
    elif query_data == "help":
        buttons = [[
            InlineKeyboardButton('पीछे जाए ⚡', callback_data='start'),
            InlineKeyboardButton('Set Caption', callback_data='caption')
        ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
        
        caption = CAPTION_DATA.get(user_id)
        caption_txt = caption.get("caption") if caption else "You have not set any caption"
        
        await update.message.edit_text(
            f"<b>Caption</b>: {caption_txt}",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )
    
    elif query_data == "caption":
        buttons = [[
            InlineKeyboardButton('पीछे जाए ⚡', callback_data='start'),
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        
        await update.message.edit_text(
            f"<b>Set Caption</b>: Send your desired caption as a separate message.",
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML,
            disable_web_page_preview=True
        )

@Client.on_message(filters.text & ~filters.command)
async def handle_text_message(bot, message):
    user_id = message.from_user.id
    caption_data = CAPTION_DATA.get(user_id)
    if caption_data:
        caption = caption_data.get("caption")
        await message.reply_text(
            text=message.text,
            caption=caption
        )
    else:
        await message.reply_text(
            text=message.text
        )
