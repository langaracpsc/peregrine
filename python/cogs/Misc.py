import time
import asyncio

import discord
from discord.ext import commands
from better_profanity import profanity

'''
Some miscellanous commands.
'''
class Misc(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
             
    # sends or edits rules for #ephemeral
    @commands.slash_command(description="🏓")
    async def ping(self, interaction:discord.Interaction, message:str):
        interaction.respond("Pong!")
            
def setup(bot:commands.Bot):
    bot.add_cog(Misc(bot))