import os
import json
from discord.ext import commands
from bot_modules.LinkingModule import LinkingModule
from db.dao import DAO
from bot_modules.SetupModule import SetupModule
from bot_modules.ProgressModule import ProgressModule

if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
    f = open(os.path.join(os.path.dirname(__file__),"config.json"))
    data = json.load(f)
    f.close()

def load(key):
    return os.getenv(key) or data[key]

class LeetcodeBot(commands.Bot):

    CONFIG = {
        'command_prefix' : '.',
        'admin_ids' : [int(curr_id) for curr_id in load("ADMIN_IDS").split(',')],
        'bot_modules' : [
            SetupModule, 
            ProgressModule, 
            LinkingModule
        ]
    }

    def __init__(self):
        super().__init__(command_prefix=self.CONFIG.get('command_prefix'))

        self.owner_ids = self.CONFIG.get('admin_ids')
        self.dao = DAO()
        
        for module in self.CONFIG.get('bot_modules'):
            self.add_cog(module(self))
