from pyrogram import filters
from pyrogram.types import Message
from ..lolBot import lolBot

@lolBot.on_message(filters.command("start") & filters.private, group=1)
async def _(client: lolBot, message: Message):
    
    msg = f'**HEY WELCOME {message.from_user.first_name}!**\n\
to use this bot you must write:\n\
@LoLUserStatsBot info SummonerName\
    '
    
    await message.reply(msg)

    