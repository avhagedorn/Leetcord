import discord
from discord.ext import commands

class SetupModule(commands.Cog):

    """
        The initial Setup Module for this bot.
    """
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.wait_until_ready()
        print(f"{self.client.user} is online")
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f"{self.client.dao.GetMemberCount()} Verified LeetCoders!"))
    