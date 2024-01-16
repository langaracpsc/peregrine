import time
import discord

from discord import option
from discord.ext import commands

import os
import requests

from main import extensions # DO NOT DELETE THIS LINE OR COG RELOAD BREAKS
# I DO NOT KNOW WHY

EMBED_TITLE = "Peregrine Admin Panel"
EMBED_DESCRIPTION = "Docker Update calls watchtower and asks it to look for updates to any docker images. Reload Peregrine Cogs attempts to hot-reload all code in cogs (but doesn't seem to be functional). The trash icon deletes the last shown log."

# helper function for displaying the last log in the selected adminpanelview
async def replaceEmbed(embedMessage:discord.Message, fieldTitle = None, runRequester = None, fieldText = None) -> discord.Embed:
    embed = discord.Embed(
        title=EMBED_TITLE, 
        description=EMBED_DESCRIPTION
        )
    
    if fieldTitle != None and runRequester != None and fieldText != None:
        embed.add_field(name=fieldTitle, value=runRequester + "\n" + fieldText)
    
    await embedMessage.edit(embed=embed)

class AdminPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 

    @discord.ui.button(label="Docker Update", custom_id="docker_update", style=discord.ButtonStyle.green)
    async def docker_update(self, button, interaction:discord.Interaction):

        fieldTitle = f"Docker Update"
        runRequester = f"Requested by <@{interaction.user.id}> at {time.strftime('%H:%M:%S', time.localtime())}."
        
        if os.getenv("WATCHTOWER_HTTP_API_TOKEN") == None:
            await replaceEmbed(interaction.message, fieldTitle, runRequester, "ERROR: No watchtower token present.")

        else:
            
            try:
                url     = 'https://watchtower.langaracs.tech/v1/update'
                headers = {"Authorization": f"Bearer {os.getenv('WATCHTOWER_HTTP_API_TOKEN')}"}
                # go in this order so that the message actually makes it to discord
                
                await replaceEmbed(interaction.message, fieldTitle, runRequester, "Sending update request...")
                
                # we must reply to discords request within 3 seconds, and the post can take longer than that
                await interaction.response.defer()
                
                result = requests.post(url, headers=headers)
                
                await replaceEmbed(interaction.message, fieldTitle, runRequester, f"Response: {result.status_code}." + "🎉" if result.status_code==200 else "")
                
                return # don't go to the defer at end since we already did that
            
            except Exception as e:
                await replaceEmbed(interaction.message, fieldTitle, runRequester, "Could not establish a connection: " + str(e))
               
        # Not what defer means, but discord expects a response and this is how you use it according to stackoverflow
        await interaction.response.defer() 

    @discord.ui.button(label="Reload Peregrine Cogs", custom_id="reload_cogs", style=discord.ButtonStyle.green)
    async def reload_cogs(self, button:discord.Button, interaction:discord.Interaction):
        
        fieldTitle = f"Reload Peregrine Cogs"
        runRequester = f"Requested by <@{interaction.user.id}> at {time.strftime('%H:%M:%S', time.localtime())}."

        # time how long cog reload takes
        start = time.time()
        
        await replaceEmbed(interaction.message, fieldTitle, runRequester, "Reloading extensions...")

        # TODO: fix this
        # deeply cursed, this is very bad
        from main import reload_all_extensions
        count = reload_all_extensions()
        
        end = str(time.time() - start)[:4]         
        await replaceEmbed(interaction.message, fieldTitle, runRequester, f"Reloaded {count} extensions in {end} seconds.")
        
        await interaction.response.defer() 
        
    @discord.ui.button(label="🗑️", custom_id="delete_log", style=discord.ButtonStyle.gray)
    async def delete_log(self, button:discord.Button, interaction:discord.Interaction):
        await replaceEmbed(interaction.message)
        await interaction.response.defer()

        

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO: write permission check so only user with certain roles can use this menu
    @commands.slash_command(description="Create Admin Panel.")
    @discord.default_permissions(administrator=True)
    async def create_admin_panel(self, ctx):
        
        embed = discord.Embed(
            title=EMBED_TITLE, 
            description=EMBED_DESCRIPTION
        )

        await ctx.respond(embed=embed, view=AdminPanelView())    
    
def setup(bot:commands.Bot):
    bot.add_cog(Admin(bot))