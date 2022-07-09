import os
import json

from discord.ext import commands
from ProgressModule import ProgressModule
from leetcode_service.leetcode_client import LeetcodeClient

if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
    f = open(os.path.join(os.path.dirname(__file__),"config.json"))
    data = json.load(f)
    f.close()

def load(key):
    return os.getenv(key) or data[key]

IS_TEST = os.getenv('DISCORD_TOKEN') == None

TOKEN = load('DISCORD_TOKEN')

class LeetcodeBot(commands.Bot):

    CONFIG = {
        'command_prefix' : '.',
    }

    def __init__(self):
        super().__init__(command_prefix=self.CONFIG['command_prefix'])

        self.add_cog(ProgressModule(self))

lcb = LeetcodeBot()

@lcb.event
async def on_ready():
    print(f"{lcb.user} is online")

if IS_TEST:
    lcb.run(TOKEN)
