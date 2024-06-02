import discord
from discord.ext import commands

'''
An example of how to implement a cog.
'''

# All cog commands are placed into a class
class Example(commands.Cog):
    # Required boilerplate for all cogs
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    
    # Your command here
    # the @ denotes a decorator which comes before your function
    @commands.slash_command(description="🏓")
    
    # your function here takes an interaction, which you will use to reply
    async def ping(self, ctx: discord.ApplicationContext):
        ctx.respond("Pong!")
            
            
# More boilerplate
def setup(bot:commands.Bot):
    bot.add_cog(Example(bot))