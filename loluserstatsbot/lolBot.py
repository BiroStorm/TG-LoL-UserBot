from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton
from pyrogram import __version__
from pyrogram.raw.all import layer
from riotwatcher import LolWatcher, ApiError
import configparser


class lolBot(Client):
    CREATOR_ID = 510456529
    
    def __init__(self):
        name = self.__class__.__name__.lower()
        print(name)
        super().__init__(
            name,
            config_file="loluserstatsbot/config.ini",
            plugins=dict(
                root="loluserstatsbot/plugins"
            ))
        


    async def start(self):
        await super().start()

        print('Loading the essentials...')

        config = configparser.ConfigParser()
        config.read('loluserstatsbot/config.ini')
        if 'lolAPI' in config.sections() and 'KEY' in config['lolAPI']:
            self.lolWatcher = LolWatcher(config['lolAPI']['KEY'])
            try:
                self.lolWatcher.summoner.by_name('na1', 'pseudonym117')
            except ApiError as err:
                if err.response.status_code == 403:
                    print("Wrong League of Legends API Key under [lolAPI] in config.ini. Please Check!")
                    exit(-1)
        else:
            print("Missing League of Legends API Key under [lolAPI] in config.ini")
            exit(0)
                   
        print('configuration completed!')

        me = await self.get_me()
        print(f"Custom Bot v{__version__} (Layer {layer}) started on @{me.username}. Hi.")


    async def stop(self, *args):
        await super().stop()
        print("The Bot has been stopped!")

    #UTILITY SECTION
    def invertCBQBool(self, inlineKeyboardButton):
        if inlineKeyboardButton.callback_data.split(' ')[-1] == "false":
            newcallback = inlineKeyboardButton.callback_data.rsplit(' ', 1)[
                0] + " true"
            newbutton = inlineKeyboardButton.text.rsplit(' ', 1)[0] + " ✅"
        else:
            newcallback = inlineKeyboardButton.callback_data.rsplit(' ', 1)[
                0] + " false"
            newbutton = inlineKeyboardButton.text.rsplit(' ', 1)[0] + " ❌"

        return InlineKeyboardButton(newbutton, newcallback)

    @staticmethod
    def CBFilter(data):
        return filters.create(
            lambda flt, query: flt.data.lower() == query.data.split(' ', 1)[0].lower() and query.message.from_user.is_self,
            data=data  # "data" kwarg is accessed with "flt.data" above
    )
