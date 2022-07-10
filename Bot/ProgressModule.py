import discord
from discord.ext import commands
from db.db_utils import standardize_difficulty
from db.models import Member, Solve
from datetime import datetime

from leetcode_service.leetcode_client import LeetcodeClient

class ProgressModule(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="solved", aliases=["s", "slvd"])
    async def solved(self, ctx, *args):
        user = self.client.dao.GetMember(ctx.message.author.id)

        if user:

            n_args = len(args)

            if n_args:
                problem_query = f"{' '.join(args)}"

                question = self.client.dao.GetProblem(problem_query, n_args)

                if not question:
                    question = LeetcodeClient.GetQuestionFromSearch(problem_query)
                    self.client.dao.MakeProblem(question)

                # num = question.problem_number
                # title = question.problem_name
                # slug = question.slug
                # difficulty = standardize_difficulty(question.difficulty)
                # premium = question.premium
                # url = question._url()

                solved = self.client.dao.Solved(user, question)

                # await ctx.send(f"{num}. {title}\n{difficulty}\n{'🔒 Premium' if premium else '🔓 Free'}\n{url}")
                await ctx.author.send(f"Congrats! 🎉\nYou just solved {question.problem_name}.\nYour solved ID is: {solved.id}\nGo to https://leetcode-discord.herokuapp.com/solution/{solved.id}")
            else:
                await ctx.send("dumbass bitch idiot add some question info")

        else:
            await ctx.send("Join the cool kids club first")


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

    @commands.command(name="neetcode", aliases=["nc"])
    async def neetcode(self, ctx):
        await ctx.send(f"🚀 https://neetcode.io/ 🚀")

    @commands.command(name="leetcode", aliases=["lc"])
    async def leetcode(self, ctx):
        await ctx.send(f"🤔 https://leetcode.com/problemset/all 🤔")

