import logging
from AutoPost.database import Database
from AutoPost.user import UserBot as Bot
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from AutoPost.helper_func import channels_pagination_callback

logger = logging.getLogger(__name__)
db = Database()

@Client.on_message(filters.private & filters.command("start"))
async def start(bot, message):
    buttons = [
        [
            InlineKeyboardButton('Set Forward', callback_data='set_forward')
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
    user_id = str(cb.message.chat.id)
    
    if query_data == 'set_forward':
        channel_id = await cb.message.chat.ask("Send me your 'from' Channel ID starting with -100:", parse_mode=enums.ParseMode.HTML)
        channel_id = from_chat_id.text.strip()
        
        if not channel_id.isdigit() or not from_chat_id.startswith("-100"):
            return await cb.message.reply_text("Invalid Channel ID. Please enter a valid Channel ID")
        
        if len(channel_id) > 14:
            return await cb.message.reply_text("Invalid Chat ID...\nChat ID should be something like this: <code>-100xxxxxxxxxx</code>")
        
        try:
            chat = await client.get_chat(int(channel_id))
            if chat.type != enums.ChatType.CHANNEL:
                return await cb.message.reply_text("This is not a valid channel ID. Please provide a channel ID.")
            if not await client.get_chat_member(chat.id, "me"):
                return await cb.message.reply_text("I am not an admin in the specified channel. Please make sure I am added as an admin.")
        except Exception as e:
            return await cb.message.reply_text(f"An error occurred while validating the channel ID: {str(e)}")
        channel_id = str(chat.id)
        db.save_chat_ids(user_id, channel_id)
        get_data = db.get_chat_ids(channel_id)
        if get_data:
            await cb.message.reply_text("Channel successfully added. You can now manage your channel from the bot's private messages.")
        else:
            await cb.message.reply_text("You have already added this channel.")

        
    elif query_data.startswith("managecl"):
        channel_id = query_data.split("#")[1]  
        chat = await client.get_chat(int(channel_id))
        channel_id = str(chat.id)
        chat_title = chat.title 
        chat_info = [chat_title, channel_id]
        await cb.message.edit_text(
            text=f"{chat.title}\nNow Manage Your Channel")
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("Auto Caption", callback_data=f"auto_caption#{chat_info}"),
                InlineKeyboardButton("Auto Forward", callback_data=f"auto_forward#{channel_id}")
                ],[
                InlineKeyboardButton("Auto Forward", callback_data='back_managecl') 
                ]]
                )
        )
    elif query_data.startswith("auto_caption"):
        chat_info = query_data.split("#")[1]      
        await cb.message.edit_text(
            text=f"{chat_info[0]}\nNow Set Caption For Your Channel")
            reply_markup=InlineKeyboardMarkup( [[
                InlineKeyboardButton("Set Caption", callback_data=f"auto_caption#{chat_info}"),
                InlineKeyboardButton("Replace Text", callback_data=f"auto_forward#{chat_info}")
                ],[
                InlineKeyboardButton("Caption Position", callback_data=f"cap_osition#{chat_info}") 
                ],[
                InlineKeyboardButton("Close", callback_data="close"),
                InlineKeyboardButton("Back", callback_data=f"managecl#{chat_info}") 
                ]]
                )                         

                                             

                


    elif query_data == "close":
        await cb.message.delete() 
    
