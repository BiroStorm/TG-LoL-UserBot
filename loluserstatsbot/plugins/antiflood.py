from pyrogram import filters
from pyrogram.types import Message
from ..lolBot import lolBot
import threading
import time

users = []

@lolBot.on_message(group=0)
async def globalFloodPrevention(client: lolBot, message: Message):
    if message.from_user.id in users: message.stop_propagation()

    users.append(message.from_user.id)
    t = threading.Thread(target = handleFlood, args=(message.from_user.id,), daemon=True)
    t.start()
    message.continue_propagation()
        
#handle the removing part from list.
def handleFlood(id):
    time.sleep(3) 
    users.remove(id)