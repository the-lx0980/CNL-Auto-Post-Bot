import logging
from AutoPost.database import Database
from AutoPost.user import UserBot as Bot
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from AutoPost.helper_func import captin_status, set_auto_caps

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
        channel_id = channel_id.text.strip()
        
        if not channel_id.startswith("-100"):
            return await cb.message.reply_text("Invalid Channel ID. Please enter a valid Channel ID With '-100'")
        
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
        db.save_channel_id(user_id, channel_id)
        get_data = db.get_channel_id(channel_id)
        if get_data:
            await cb.message.reply_text(f"{get_data} Channel successfully added. You can now manage your channel from the bot's private messages.")
        else:
            await cb.message.reply_text("You have already added this channel.")

        
    elif query_data.startswith("managecl"):
        _id = query_data.split("#")[1]  
        _name = query_data.split("#")[2]
        await cb.message.edit_text(
            text=f"{_name}\nNow Manage Your Channel",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Auto Caption", callback_data=f"auto_caption#{_id}#{_name}")
                ]
            ])
        )
    elif query_data.startswith("auto_caption"):
        _id = query_data.split("#")[1]
        _name = query_data.split("#")[2]      
        await cb.message.edit_text(
            text=f"<b>{_name}</b>\nNow Set Caption For Your Channel",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Caption", callback_data=f"set_caption#{_id}")
                ]
            ])
        )

    elif query_data.startswith("set_caption"):
        _id = query_data.split("#")[1]     
        msg = cb.message 
        try:
            chat = await client.get_chat(int(_id))
            channel_id = str(chat.id)
            get_cap = db.get_auto_cap(channel_id)
            if not get_cap:
                cap_ask = await msg.chat.ask("Now send Your Channel Caption", parse_mode=enums.ParseMode.HTML)
                auto_caption = cap_ask.text
                if auto_caption:
                    await cap_ask.delete()
                db.set_auto_cap(channel_id, auto_caption)
                get_cap = db.get_auto_cap(channel_id)
                if get_cap:
                    edit_status = f"<b>{chat.title}</b>\n\n<b>Caption:</b> {auto_caption}"
                    buttons = [[
                        InlineKeyboardButton('Delete Caption', callback_data='close')
                    ],[
                        InlineKeyboardButton('Back', callback_data=f'auto_caption#{_id}#{chat.title}')
                    ]]
                    await cb.answer(f"Your Caption Is Successfully Set!\n\n{auto_caption}", show_alert=True)
                    await client.send_message(
                        chat_id=msg.id,
                        text=edit_status,
                        reply_markup=InlineKeyboardMarkup(buttons)
                    )
                else:
                    await msg.reply_text("Your Caption Is Not set")
        except Exception as e:
            await msg.reply_text(f'Error - {e}')
        
    elif query_data == "close":
        await cb.message.delete() 
