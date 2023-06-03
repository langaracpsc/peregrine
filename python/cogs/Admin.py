import discord
from discord.ext import commands
import os
import requests

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Executes code on the server
    @commands.slash_command(description="For administrative purposes only.")
    @discord.default_permissions(administrator=True)
    async def execute(self, interaction:discord.Interaction, message):
        try:
            exec(message)
            await interaction.respond(f"Executed `{message}`", ephemeral=True)
        except:
            await interaction.respond("Execution failed.", ephemeral=True)

    # Asks watchtower to check for updates
    @commands.slash_command(description="Updates docker containers if an update exists")
    @discord.default_permissions(administrator=True)
    async def update_docker(self, interaction:discord.Interaction):
        if os.getenv("WATCHTOWER_HTTP_API_TOKEN") == None:
            await interaction.respond("No watchtower token present.", ephemeral=True)
        else:
            try:
                url     = 'http://localhost:8080/v1/update'
                headers = {"Authorization": f"Bearer {os.getenv('WATCHTOWER_HTTP_API_TOKEN')}"}
                # go in this order so that the message actually makes it to discord
                requests.post(url)
                await interaction.respond("Update request sent to the cloud.")
                await requests.post(url, headers=headers)
            except Exception as e:
                await interaction.respond("Could not establish a connection: " + str(e))

def setup(bot:commands.Bot):
    bot.add_cog(Admin(bot))