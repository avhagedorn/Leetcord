import discord
from discord.ext import commands
from embed_util import difficulty_color
from db.db_utils import standardize_difficulty

from leetcode_service.leetcode_client import LeetcodeClient

class LinkingModule(commands.Cog):

    """
        The external linking interface for Leetcord.
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="neetcode", 
        aliases=["nc"],
        brief="Link to Neetcode.",
        description="An excellent selection of leetcode questions."
    )
    async def neetcode(self, ctx):
        embed = discord.Embed(colour=0xff9d5c,title="🚀 Neetcode",description="An excellent selection of leetcode questions.",url="https://neetcode.io/")
        await ctx.send(embed=embed)

    @commands.command(
        name="leetcode", 
        aliases=["lc"],
        brief="Link to Leetcode.",
        description="Your one-stop-shop for coding problems."
    )
    async def leetcode(self, ctx):
        embed = discord.Embed(colour=0xff9d5c,title="Leetcode",description="Your one-stop-shop for coding problems.",url="https://leetcode.com/problemset/all")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(
        name="about", 
        brief="About Leetcord.",
        description="A tracking solution for leetcode."
    )
    async def about(self, ctx):
        embed = discord.Embed(colour=0xff9d5c,title="About",description="Your one-stop-shop for coding problems.",url="https://leetcord.herokuapp.com/about")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(
        name="dailyquestion",
        aliases=["daily", "questionoftoday", "today","dq"],
        brief="The question of the day.",
        description="Fetches the question of the day from Leetcode."
    )
    async def dailyquestion(self, ctx):
        question = LeetcodeClient.GetQuestionOfToday()

        # TODO: Optimize this if possible, also edit embed.
        problem = self.client.dao._GetProblemByNumber(question.problem_number)
        if not problem:
            self.client.dao.MakeProblem(question)
        embed = discord.Embed(
            url=question._url(),
            title=question.problem_name,
            colour=difficulty_color(question.difficulty),
            description=f"Today's daily question is {question.problem_number}. {question.problem_name}"
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="random",
        aliases=["r", "randomquestion"],
        brief="A random question.",
        description="Use `.random [easy/medium/hard] [premium]`."
    )
    async def random(self, ctx, difficulty=None, is_premium=None):
        if is_premium:
            is_premium = is_premium.lower()
        is_premium = is_premium == "true" or is_premium == "premium"
        
        difficulty = standardize_difficulty(difficulty.title())
        question = self.client.dao.GetRandomProblem(difficulty, is_premium)
        # embed = discord.Embed(
        #     url=question._url(),
        #     title=question.problem_name,
        #     colour=difficulty_color(question.difficulty),
        #     description=f"Your random question is {question.problem_number}. {question.problem_name}"
        # )
        # await ctx.send(embed=embed)
