from AutoPost.database import Database
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

db = Database()


async def captin_status(client, cb, query_data, _id):
    msg = cb.message
    channel_id = str(_id)
    get_cap = db.get_auto_cap(channel_id)
    try:
        chat = await client.get_chat(int(_id))
    except:
        return await msg.reply_text("I'm Not Admin In Your Channel")    
    try:
        if get_cap: 
            buttons = [[
                InlineKeyboardButton('Delete Caption', callback_data=f'del_caption#{_id}')
            ],[
                InlineKeyboardButton('Back', callback_data=f'auto_caption#{_id}')
            ]]
            text = f"<b>Channel:</b> {chat.title}\n\nCaption:</b> {get_cap}"
            await msg.edit_text(
                chat_id=nsg.id,
                text=text,
                reply_markup=InlineKeyboardMarkup(buttons) 
            )
            return
        
        buttons = [[
            InlineKeyboardButton('Set Caption', callback_data=f'set_caption#{_id}')
        ],[
            InlineKeyboardButton('Back', callback_data=f'auto_caption#{_id}')
        ]]
        text = f"<b>Channel:</b> {chat.title}\n\n<b>Caption:</b> You have not set any caption."
        await msg.edit_text(
            chat_id=nsg.id,
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons) 
        )
    except Exception as e:
        await msg.reply_text(f'Error - {e}')

            
            
            
