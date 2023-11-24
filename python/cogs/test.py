import discord
from discord.ext import commands
import os
import requests

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Executes code on the server
    @commands.slash_command(description="For administrative purposes only.")
    @discord.default_permissions(administrator=True)
    async def execute(self, interaction:discord.Interaction, message):
        interaction.respond("HI")

def setup(bot:commands.Bot):
    bot.add_cog(Test(bot))