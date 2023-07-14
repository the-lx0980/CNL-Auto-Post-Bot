from AutoPost.database import Database
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

db = Database()


async def set_auto_caps(client, cb, query_data, _id):
    msg = cb.message
    await msg.delete()
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
