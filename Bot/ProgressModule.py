from typing import List
import discord
from discord.ext import commands
from embed_util import difficulty_color
from db.db_utils import standardize_difficulty
from db.models import Member
from datetime import datetime

from leetcode_service.leetcode_client import LeetcodeClient

class ProgressModule(commands.Cog):

    """
        The data interface for Leetcord. Adds, removes, and modifies data and reflects it on the web-application: https://leetcode-discord.herokuapp.com/
    """

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="solved", 
        aliases=["s", "slvd"],
        brief="Adds a solution to your account.",
        description="If the user is registered they can run this command by doing `.solved <Leetcode Number/Leetcode Slug/Leetcode URL>` to add a solution to the database. On success the command will send an embed containing a link to the solution. Otherwise, if it fails, the command will indicate as such."
    )
    async def solved(self, ctx, *args):
        user = self.client.dao.GetMember(ctx.message.author.id)

        if user:

            n_args = len(args)

            if n_args:
                problem_query = f"{' '.join(args)}"

                question = self.client.dao.GetProblem(problem_query, n_args)

                if not question:
                    try:
                        question = LeetcodeClient.GetQuestionFromSearch(problem_query)
                        self.client.dao.MakeProblem(question)
                    except Exception as e:
                        print(e)
                        await ctx.reply("An unexpected error occurred. If this issue persists, contact Alan or Kanishk.")
                    
                solved = self.client.dao.Solved(user, question)

                embed = discord.Embed(colour=difficulty_color(question.difficulty),title="Solution Added!",url=f"https://leetcode-discord.herokuapp.com/solution/{solved.id}",description=f"Congratulations on solving Leetcode {standardize_difficulty(question.difficulty)} {question.problem_number} : {question.problem_name}.\nClick on the title to see your solution!\nDo `.takeaway {solved.id} \"YOUR TAKEAWAY\"` to add a takeaway.\nDo `.delete {solved.id}` to remove your solution.")
                embed.set_author(name=user.discordName,url=f"https://leetcode-discord.herokuapp.com/member/{user.discordID}",icon_url=user.discordPFP)

                if question.premium:
                    embed.set_footer(text="This is a premium question.")

                await ctx.reply(embed=embed)
            else:
                await ctx.reply("No information was provided, couldn't indentify a leetcode question.")
        else:
            await ctx.reply("You haven't been verified yet, contact Alan or Kanishk to get verification.")

    @commands.command(
        name="takeaway",
        aliases=["t", "tkwy"],
        brief="Adds a takeaway to your solution.",
        description="If the user is registered and is associated with a solution they can run this command by doing `.takeaway <SolvedID> <Takeaway>` to add a takaway to the solution. On success the command will send an embed containing a link to the solution. Otherwise, if it fails, the command will indicate as such."
    )
    async def takeaway(self, ctx, *args):
        user = self.client.dao.GetMember(ctx.message.author.id)

        if user:
            if len(args) > 1 and args[0].isnumeric():
                solution_id, *rest = args
                solution_id = int(solution_id)
                takeaway = ' '.join(rest)

                solution = self.client.dao.GetSolution(solution_id)

                if solution:
                    if solution.solvee == user:
                        solution = self.client.dao.UpdateTakeaway(solution, takeaway)

                        embed = discord.Embed(colour=difficulty_color(solution.problem.difficulty),title="Takeaway Updated!",url=f"https://leetcode-discord.herokuapp.com/solution/{solution.id}",description=f"Takway updated successfully.\nClick on the title to see your solution!\nDo `.takeaway {solution.id} \"YOUR TAKEAWAY\"` to update this takeaway.\nDo `.delete {solution.id}` to remove your solution.")
                        embed.set_author(name=user.discordName,url=f"https://leetcode-discord.herokuapp.com/member/{user.discordID}",icon_url=user.discordPFP)
                        
                        if solution.problem.premium:
                            embed.set_footer(text="This is a premium question.")

                        await ctx.reply(embed=embed)
                    
                    else:
                        await ctx.reply("Cannot modify takeaway for another user's solution!")
                else:
                    await ctx.reply("No such solution exists!")
            else:
                await ctx.reply("Not enough information was provided, or SolvedID is not valid.")
        else:
            await ctx.reply("You haven't been verified yet, contact Alan or Kanishk to get verification.")


    @commands.command(
        name="delete", 
        aliases=["d", "del"],
        brief="Deletes a solution.",
        description="Use `.delete <SolveID>` to delete a solution. The user attempting a delete must have created the solution."
    )
    async def delete(self, ctx, solution_id):
        user = self.client.dao.GetMember(ctx.message.author.id)

        if user:
            if solution_id:
                if solution_id.isnumeric():
                    solution_id = int(solution_id)
                    solution = self.client.dao.GetSolution(solution_id)

                    if solution:
                        if solution.solvee == user:
                            problem = solution.problem
                            self.client.dao.DeleteSolution(solution)    
                            await ctx.reply(f"Deleted solution with ID {solution_id} for {problem.problem_number}. {problem.problem_name}")
                        else:
                            await ctx.reply("Cannot delete a different user's solution!")
                    else:
                        await ctx.reply(f"Solution does not exist for SolveID: {solution_id}")                             
                else:
                    await ctx.reply("SolvedID was not an integer.")
            else:
                await ctx.reply("SolvedID was not provided.")
        else:
            await ctx.reply("You haven't been verified yet, contact Alan or Kanishk to get verification.")

    @commands.command(
        name="stats",
        aliases=["st"],
        brief="Gets a user's submission stats.",
        description="Use `.stats <Member>` to get a member's stats. If no member is provided, the caller's stats will be displayed."
    )
    async def command(self, ctx, discord_member: discord.User = None):

        async def display_stats(self, ctx, user):
            easy, medium, hard = self.client.dao.GetMemberStats(user)
            embed = discord.Embed(colour=0xff9d5c,title="User Stats",url=f"https://leetcode-discord.herokuapp.com/member/{user.discordID}",description=f"Total Solved: {easy+medium+hard}\nEasies Solved: {easy}\nMediums Solved: {medium}\nHards Solved: {hard}")
            embed.set_author(name=user.discordName,url=f"https://leetcode-discord.herokuapp.com/member/{user.discordID}",icon_url=user.discordPFP)
            await ctx.reply(embed=embed)

        if discord_member:
            member = self.client.dao.GetMember(discord_member.id)
            await display_stats(self, ctx, member) if member else await ctx.reply(f"@{discord_member.display_name} hasn't been verified yet, cannot fetch stats.")
        else:
            member = self.client.dao.GetMember(ctx.message.author.id)
            await display_stats(self, ctx, member) if member else await ctx.reply("You haven't been verified yet, contact Alan or Kanishk to get verification.")

    @commands.is_owner()
    @commands.command(
        name="makemember",
        brief="Creates a member in the database.",
        description="Use `.member <Member>` in order to create a new member in the database.",
        hidden=True
    )
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
    
    @commands.command(
        name="leeterboard",
        aliases=["letterboard"],
        brief="Top 5 users with most solved problems.",
        description="Top 5 users with most solved problems."
    )
    async def leeterboard(self, ctx):
        users: List[Member] = self.client.dao.GetTopUsers(limit=5)
        usersString = ""

        for i in range(len(users)):
            # TODO: fix this n+1 query yikes
            easy, medium, hard = self.client.dao.GetMemberStats(users[i])

            usersString += \
                f"""{i+1}. {users[i].discordName}
                Total Solved: {easy+medium+hard}
                Easies Solved: {easy}
                Mediums Solved: {medium}
                Hards Solved: {hard}
                ~~               ~~\n"""
        
        embed = discord.Embed(
            colour=0xff9d5c,
            title="Leeterboard",
            description=usersString
        )

        await ctx.reply(embed=embed)

    @commands.command(
        name="user",
        brief="Displays a user's information",
        description="Use `.user [Member]`. If a Member is given it will display their number of solutions as well as a link to their information. Otherwise it will display the invoker's information. If the indicated user doesn't exist it will indicate as such."
    )
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

