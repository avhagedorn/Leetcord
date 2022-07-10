import discord
from discord.ext import commands
from db.models import Member
from datetime import datetime

from leetcode_service.leetcode_client import LeetcodeClient

class ProgressModule(commands.Cog):

    """
        The data interface for Leetcord. Adds, removes, and modifies data and reflects it on the web-application: https://leetcode-discord.herokuapp.com/
    """

    DIFF_MAPPING = {
        0 : 0x00b8a3,
        1 : 0xffc01e,
        2 : 0xff375f
    }
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

