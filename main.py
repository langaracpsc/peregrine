import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv
load_dotenv()

from RolePicker import RolePicker, Role

ids = [714354863349170187, 753037165050593300, 511924606651727895]
bot = discord.Bot(owner_id=221780012372721664,debug_guilds=ids)


class RoleMenuButton(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, roles=None):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Choose Roles!", custom_id="RoleMenuButton", style=discord.ButtonStyle.success) 
    async def button_callback(self, button, interaction):

        view = RolePicker(interaction)
        await interaction.response.send_message("Pick your roles:", ephemeral=True, delete_after=300, view=view)

class ShenaniganButton(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    def __init__(self, roles=None):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="✨Get Involved!✨", custom_id="ShenaniganButton", style=discord.ButtonStyle.success) 
    async def button_callback(self, button, interaction:discord.Interaction):
        
        user_roles = []
        for role in interaction.user.roles:
            user_roles.append(str(role.id))
            
        r = interaction.guild.get_role(1040769521117569074) 
                        
        if "1040769521117569074" not in user_roles:
            await interaction.user.add_roles(r)
            await interaction.response.send_message(f"Gave you the planning role!", ephemeral=True, delete_after=5)

        else:
            await interaction.user.remove_roles(r)
            await interaction.response.send_message(f"Took away your planning role!", ephemeral=True, delete_after=5)

@bot.slash_command() # Create a slash command
async def rolemenu(ctx):
    await ctx.respond("Self-Assignable Roles!", view=RoleMenuButton()) 
    
@bot.slash_command() # Create a slash command
async def shenanigans(ctx):
    await ctx.respond("Would you like to help organize events or be involved in the club? Grab a planning role today and help us make this club better!", view=ShenaniganButton()) 

@bot.event
async def on_ready():
    bot.add_view(RoleMenuButton())
    bot.add_view(ShenaniganButton())
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


print("Running bot!")
bot.run(os.getenv("DISCORD_TOKEN"))