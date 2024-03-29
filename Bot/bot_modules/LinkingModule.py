import discord
from discord.ext import commands
from db.db_constants import Constants
from embed_util import difficulty_color
from db.db_utils import standardize_difficulty

from leetcode_service.leetcode_client import LeetcodeClient

class LinkingModule(commands.Cog):

    """
        The external linking interface for Leetcord.
    """

    async def validate_connection(self,ctx):
        if not self.client.dao._session.is_active:
            self.client.dao._session.begin()
    async def terminate_connection(self,ctx):
        self.client.dao._session.close()

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="dailyquestion",
        aliases=["daily", "questionoftoday", "today","dq"],
        brief="The question of the day.",
        description="Fetches the question of the day from Leetcode."
    )
    @commands.before_invoke(validate_connection)
    @commands.after_invoke(terminate_connection)
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
        description="Use `.random (easy/medium/hard) (premium)`. This command by default provides a random choice from non-premium questions from LeetCode. If a difficulty is provided the search will be limited to that selection. If premium is passed as a parameter the search will be expanded to include premium problems."
    )
    @commands.before_invoke(validate_connection)
    @commands.after_invoke(terminate_connection)
    async def random(self, ctx, raw_difficulty='', raw_premium=''):
        is_premium = False
        difficulty = None

        raw_premium = raw_premium.lower()
        is_premium = True if raw_difficulty == "premium" else raw_premium
        is_premium = is_premium or raw_premium == "premium"    
        difficulty = standardize_difficulty(raw_difficulty.title()) if raw_difficulty.title() in Constants.DIFFICULTY_MAPPING.values() else None

        question = self.client.dao.GetRandomProblem(difficulty, is_premium)

        embed = discord.Embed(
            url=question._url(),
            title=question.problem_name,
            colour=difficulty_color(question.difficulty),
            description=f"Your random question is {question.problem_number}. {question.problem_name}"
        )

        if question.premium:
            embed.set_footer(text="This is a premium question.")

        await ctx.reply(embed=embed)

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
        embed = discord.Embed(colour=0xff9d5c,title="About Leetcord",description="Learn more about Leetcord!",url="https://leetcord.herokuapp.com/about")
        await ctx.send(embed=embed)

