# (c) @TheLx0980

from pyrogram import filters, Client


@Client.on_message(filters.command("start") & filters.private & filters.incoming)
async def start(client, message):
    await message.reply(
        text="I'm Online",
        disable_web_page_preview=True,
        quote=True
    )


    


