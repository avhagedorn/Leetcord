import os
import json
from bot import LeetcodeBot
from HelpCommand import LeetcordHelpCommand

if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
    f = open(os.path.join(os.path.dirname(__file__),"config.json"))
    data = json.load(f)
    f.close()

def load(key):
    return os.getenv(key) or data[key]

TOKEN = load('DISCORD_TOKEN')

IS_TEST = os.getenv('DISCORD_TOKEN') == None

lcb = LeetcodeBot()
lcb.help_command = LeetcordHelpCommand()

if IS_TEST:
    lcb.run(TOKEN)
