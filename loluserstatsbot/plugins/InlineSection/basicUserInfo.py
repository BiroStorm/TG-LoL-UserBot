from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from riotwatcher import ApiError
from pyrogram import filters
from ...lolBot import lolBot
import re

# @username euw info [summonerName] 
@lolBot.on_inline_query(filters.regex("^(euw|na) info ", flags=re.IGNORECASE))
async def handleInlineQuery(client: lolBot, query: InlineQuery):
    args = query.query.split(' info ')
    if len(args[1]) < 3: return

    user = None
    errmsg = None

    try:
        if(args[0].upper() == 'EUW'):
            user = client.lolWatcher.summoner.by_name('euw1', args[1])
        elif (args[0].upper() == 'NA'):
            user = client.lolWatcher.summoner.by_name('na1', args[1])
    except ApiError as err:
            if err.response.status_code == 404:
                errmsg = f"User not found in region {args[0].upper()}"
    #if user has found
    if user: userinfo = f"Region: {args[0].upper()}\nName: {user['name']}\nLevel: {user['summonerLevel']}"
    
    #send back the result
    await query.answer(results=[
    InlineQueryResultArticle(
        f"{args[1]} Basic Information",
        InputTextMessageContent(errmsg if errmsg else userinfo))])