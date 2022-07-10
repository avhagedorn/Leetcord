from discord.ext import commands
from db.dao import DAO
from SetupModule import SetupModule
from ProgressModule import ProgressModule

class LeetcodeBot(commands.Bot):

    CONFIG = {
        'command_prefix' : '.',
        'admin_ids' : set([551602618028523546, 352144846649032707])
    }

    def __init__(self):
        super().__init__(command_prefix=self.CONFIG['command_prefix'])

        self.owner_ids = self.CONFIG.get('admin_ids')
        self.dao = DAO()
        
        self.add_cog(SetupModule(self))
        self.add_cog(ProgressModule(self))
