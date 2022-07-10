import discord
from discord.ext import commands
from db.models import Member
from datetime import datetime

from leetcode_service.leetcode_client import LeetcodeClient

class ProgressModule(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="solved", aliases=["s", "slvd"])
    async def solved(self, ctx, *args):
        user = self.client.dao.GetMember(ctx.message.author.id)
        n_args = len(args)

        if not user:
            await ctx.send("You must be a registered member of Leetcord!")
            return 

        if not n_args:
            await ctx.send("Specify a problem using the format:\n.solved <problem name / slug / url>")
            return

        problem_query = ' '.join(args)
        question = self.client.dao.GetProblem(problem_query, n_args)

        if not question:
            try:
                question = LeetcodeClient.GetQuestionFromSearch(problem_query)
                self.client.dao.MakeProblem(question)
            except Exception as e:
                print(e)
                await ctx.send("An unexpected error occurred. Please reach out if this problem persists.")
                return

        solved = self.client.dao.Solved(user, question)

        await ctx.author.send(
            f"""
            Congrats! 🎉\n
            You just solved {question.problem_name}.\n
            Your solved ID is: {solved.id}\n
            View solution at https://leetcode-discord.herokuapp.com/solution/{solved.id}
            """
        )
        return

    @commands.command(name="takeaway", aliases=["t", "tkwy"])
    async def takeaway(self, ctx, *args):
        user = self.client.dao.GetMember(ctx.message.author.id)

        if not user:
            await ctx.send("You must be a registered member of Leetcord!")
            return

        if len(args) <= 1 or not args[0].isnumeric():
            await ctx.send("Invalid input!")
            return
        
        solution_id, *rest = args
        solution_id = int(solution_id)
        takeaway = ' '.join(rest)

        solution = self.client.dao.GetSolution(solution_id)

        if not solution:
            await ctx.send("No such solution exists!")
            return

        if solution.solvee != user:
            await ctx.send("Cannot modify takeaway for another user's solution!")
            return
        
        solution = self.client.dao.UpdateTakeaway(solution, takeaway)
        await ctx.send(f"Successfully updated takeaway. View at https://leetcode-discord.herokuapp.com/solution/{solution.id}")
        return

    @commands.command(name="delete", alias=["d", "del"])
    async def delete(self, ctx, solution_id):
        user = self.client.dao.GetMember(ctx.message.author.id)

        if not user:
            await ctx.send("You must be a registered member of Leetcord!")
            return
        
        if not solution_id:
            await ctx.send("No solution ID provided!")
            return
        
        if not solution_id.isnumeric():
            await ctx.send("Solution ID must be an integer!")
            return

        solution_id = int(solution_id)
        solution = self.client.dao.GetSolution(solution_id)        

        if not solution:
            await ctx.send(f"Solution does not exist for solution ID {solution_id}")            
            return 

        self.client.dao.DeleteSolve(solution)    
        await ctx.send(f"Deleted solution with ID {solution_id}")
        return

    @commands.is_owner()
    @commands.command(name="makemember", alias=["createmember", "makeuser", "createuser"])
    async def makemember(self, ctx, member: discord.User):
        new_member = Member()
        new_member.discordID = member.id
        new_member.discordName = member.name
        new_member.discordPFP = str(member.avatar_url)
        new_member.date_verified = datetime.now()

        self.client.dao.MakeMember(new_member)

        await ctx.send(f"Created member for {member.mention}! 🎉")

    @commands.command(name="user", alias=["member"])
    async def user(self, ctx):
        user_id = ctx.message.author.id
        user = self.client.dao.GetMember(user_id)

        if user:
            await ctx.send(str(user))
        else:
            await ctx.send("You must be a registered member of Leetcord!")

    @commands.command(name="neetcode", aliases=["nc"])
    async def neetcode(self, ctx):
        await ctx.send(f"🚀 https://neetcode.io/ 🚀")

    @commands.command(name="leetcode", aliases=["lc"])
    async def leetcode(self, ctx):
        await ctx.send(f"🤔 https://leetcode.com/problemset/all 🤔")

