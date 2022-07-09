from discord.ext import commands
from db.dao import DAO

from leetcode_service.leetcode_client import LeetcodeClient

class ProgressModule(commands.Cog):

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
    @commands.command(name="makeuser")
    async def makeuser(self, ctx):
        author = ctx.message.author
        user_id = ctx.message.author.id
        user_name = ctx.message.auth

        await ctx.send("user is admin")

    
    @commands.command(name="user")
    async def user(self, ctx):
        user_id = ctx.message.author.id

        x = DAO()
        user = x.GetUser(user_id)
        await ctx.send(str(user))
