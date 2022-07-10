import discord
from discord.ext import commands
class LeetcordHelpCommand(commands.HelpCommand):

  def __init__(self):
    super().__init__()
  
  async def send_bot_help(self,mapping):
    destination = self.get_destination()
    embed = discord.Embed(colour=0xff9d5c,title="Help Menu\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    for cog in mapping:
      if len(mapping[cog]) > 0 and cog:
        cog_commands = [f"`{command.name}`\t{command.brief}" for command in cog.get_commands()]
        cog_string = "\n".join(cog_commands)
        embed.add_field(name=cog.qualified_name,value = cog_string,inline=False)
    await destination.send(embed=embed)
    return await super().send_bot_help(mapping)

  async def send_command_help(self,command):
    embed = discord.Embed(colour=0xff9d5c,title=f"Help for {command.name}",description=command.description)
    await self.get_destination().send(embed=embed)
    return await super().send_command_help(command)

  async def send_cog_help(self,cog):
    embed = discord.Embed(colour=0xff9d5c,title=f"Help for {cog.qualified_name}",description=cog.description)
    await self.get_destination().send(embed=embed)
    return await super().send_cog_help(cog)