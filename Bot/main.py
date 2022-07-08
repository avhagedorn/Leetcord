import os
from dotenv import load_dotenv

import discord
from discord.ext import commands
from leetcode_service.leetcode_client import LeetcodeClient

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class LeetcodeBot(commands.Bot):

    CONFIG = {
        'command_prefix' : '.',
    }

    def __init__(self):
        super().__init__(command_prefix=self.CONFIG['command_prefix'])

lcb = LeetcodeBot()

@lcb.event
async def on_ready():
    print(f"{lcb.user} is online")

@lcb.command(name="solved", aliases=["s", "slvd"])
async def solved(ctx, arg):
    if arg.isnumeric():
        pass
    else:
        question = LeetcodeClient.GetQuestion(arg)
        await ctx.send(f"{question.title}\n{question.difficulty}\n{question.url}")

lcb.run(TOKEN)