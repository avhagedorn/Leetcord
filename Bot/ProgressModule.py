import discord
from discord.ext import commands
from db.db_utils import standardize_difficulty
from db.models import Member, Solve
from datetime import datetime

from leetcode_service.leetcode_client import LeetcodeClient

class ProgressModule(commands.Cog):

    DIFF_MAPPING = {
        0 : 0x00b8a3,
        1 : 0xffc01e,
        2 : 0xff375f
    }
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
                
                embed = discord.Embed(colour=self.DIFF_MAPPING[question.difficulty],title="Solution Added!",url=f"https://leetcode-discord.herokuapp.com/solution/{solved.id}",description=f"Congratulations on solving Leetcode {standardize_difficulty(question.difficulty)} {question.problem_number} : {question.problem_name}.\nClick on the title to see your solution!\nDo `.takeaway {solved.id} \"YOUR TAKEAWAY\"` to add a takeaway.\nDo `.delete {solved.id}` to remove your solution.")
                embed.set_author(name=user.discordName,url=f"https://leetcode-discord.herokuapp.com/member/{user.discordID}",icon_url=user.discordPFP)
                if question.premium:
                    embed.set_footer(text="This is a premium question.")


                await ctx.reply(embed=embed)
            else:
                await ctx.reply("No information was provided, couldn't indentify a leetcode question.")

        else:
            await ctx.reply("You haven't been verified yet, contact Alan or Kanishk to get verification.")


    @commands.is_owner()
    @commands.command(name="makemember")
    async def makemember(self, ctx, member: discord.User):
        new_member = Member()
        new_member.discordID = member.id
        new_member.discordName = member.name
        new_member.discordPFP = str(member.avatar_url)
        new_member.date_verified = datetime.now()
        new_member.num_solutions = 0

        self.client.dao.MakeMember(new_member)
        embed = discord.Embed(colour=0xff9d5c,title="User Creation Successful!",description=f"Number of Solutions : {new_member.num_solutions}")
        embed.set_author(name=new_member.discordName,url=f"https://leetcode-discord.herokuapp.com/member/{new_member.discordID}",icon_url=new_member.discordPFP)
        embed.set_footer(text=f"Verified on {new_member.date_verified}")

        await ctx.reply(embed=embed)


    @commands.command(name="user")
    async def user(self, ctx, member: discord.User = None):
        if member:
            user_id = member.id
        else:
            user_id = ctx.message.author.id
        user = self.client.dao.GetMember(user_id)
        if user:
            embed = discord.Embed(colour=0xff9d5c,description=f"Number of Solutions : {user.num_solutions}",url=f"https://leetcode-discord.herokuapp.com/member/{user.discordID}")
            embed.set_author(name=user.discordName,url=f"https://leetcode-discord.herokuapp.com/member/{user.discordID}",icon_url=user.discordPFP)
            embed.set_footer(text=f"Verified on {user.date_verified}")
            await ctx.send(embed=embed)
        else:
            await ctx.reply("Unfortunately your account has not been verified yet")

    @commands.command(name="neetcode", aliases=["nc"])
    async def neetcode(self, ctx):
        embed = discord.Embed(colour=0xff9d5c,title="🚀 Neetcode",description="An excellent selection of leetcode questions.",url="https://neetcode.io/")
        await ctx.send(embed=embed)

    @commands.command(name="leetcode", aliases=["lc"])
    async def leetcode(self, ctx):
        embed = discord.Embed(colour=0xff9d5c,title="Leetcode",description="Your one-stop-shop for coding problems.",url="https://leetcode.com/problemset/all")
        embed.set_thumbnail(url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

