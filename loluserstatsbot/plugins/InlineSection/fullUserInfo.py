from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, InlineQuery
from riotwatcher import ApiError
from pyrogram import filters
from ...lolBot import lolBot
import re

# @username euw full [summonerName]

@lolBot.on_inline_query(filters.regex("^(euw|na) full ", flags=re.IGNORECASE))
async def fullSearchAccount(client: lolBot, query: InlineQuery):
    args = query.query.split(' full ')
    if len(args[1]) < 3:
        return
    errmsg = None
    try:
        if(args[0].upper() == 'EUW'):
            user = client.lolWatcher.summoner.by_name('euw1', args[1])
            advancedData = client.lolWatcher.league.by_summoner('euw1', user['id'])
            #sorted(champMastery, key=lambda x: x['championPoints'], reverse=True)
            
        elif (args[0].upper() == 'NA'):
            user = client.lolWatcher.summoner.by_name('na1', args[1])
            advancedData = client.lolWatcher.league.by_summoner('na1', user['id'])
        
    except ApiError as err:
        if err.response.status_code == 404:
            errmsg = f"User not found in region {args[0].upper()}"
            
    #if there is no error -> create the text to return to the user.       
    if not errmsg:
        userinfo = f"**Region**: {args[0].upper()}\n\
**Name**: {user['name']}\n\
**Level**: {user['summonerLevel']}\n"

        #advancedData will be [] if the player has not joined a tier.
        if advancedData:
            for item in advancedData:
                userinfo = userinfo + f"**=====================**\n\
**Game**: {item['queueType']}\n\
**Tier**: {item['tier']} {item['rank']}\n\
**Wins**: {item['wins']}\n\
**Losses**: {item['losses']}\n"
        else:
            userinfo = userinfo + f"{args[1]} Has not ranked yet."

    # send back the result
    await query.answer(results=[
        InlineQueryResultArticle(
            f"{args[1]} Full Information",
            InputTextMessageContent(errmsg if errmsg else userinfo))])
