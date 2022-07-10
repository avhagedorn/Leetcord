import os
import json
from bot import LeetcodeBot

if os.path.exists(os.path.join(os.path.dirname(__file__),"config.json")):
    f = open(os.path.join(os.path.dirname(__file__),"config.json"))
    data = json.load(f)
    f.close()

def load(key):
    return os.getenv(key) or data[key]

IS_TEST = os.getenv('DISCORD_TOKEN') == None
TOKEN = load('DISCORD_TOKEN')

lcb = LeetcodeBot()

@lcb.event
async def on_ready():
    print(f"{lcb.user} is online")

if IS_TEST:
    lcb.run(TOKEN)
