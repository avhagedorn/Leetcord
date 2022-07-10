import discord
from discord.ext import commands
from db.models import Member
from db.dao import DAO
from datetime import datetime

from leetcode_service.leetcode_client import LeetcodeClient

class ProgressModule(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="solved", aliases=["s", "slvd"])
    async def solved(self, ctx, *args):
        
        user_id = ctx.message.author.id
        problem_query = f"{' '.join(args)}"

        problem = None # TODO: query from Azure

        if not problem:
            # TODO: query from lc, save to Azure
            question = LeetcodeClient.GetQuestionFromSearch(problem_query)

            await ctx.send(f"{question.title}\n{question.difficulty}\n{question.url}")


    @commands.is_owner()
    @commands.command(name="makemember")
    async def makemember(self, ctx, member: discord.User):
        new_member = Member()
        new_member.discordID = member.id
        new_member.discordName = member.name
        new_member.discordPFP = str(member.avatar_url)
        new_member.date_verified = datetime.now()

        self.client.dao.MakeMember(new_member)

        await ctx.send(f"Created member for {member.mention}! 🎉")


    @commands.command(name="user")
    async def user(self, ctx):
        user_id = ctx.message.author.id
        user = self.client.dao.GetMember(user_id)
        await ctx.send(str(user))
