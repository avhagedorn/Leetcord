from discord.ext import commands

from leetcode_service.leetcode_client import LeetcodeClient

class ProgressModule(commands.Cog):

    @commands.command(name="solved", aliases=["s", "slvd"])
    async def solved(self, ctx, arg):
        question = LeetcodeClient.GetQuestionFromSearch(arg)
        await ctx.send(f"{question.title}\n{question.difficulty}\n{question.url}")
