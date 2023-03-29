import discord
from discord.ext import commands

from cogs.RolePicker import RoleMenuButton


class OnboardingMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()  # Not passing in guild_ids creates a global slash command.
    async def hi(self, ctx: discord.ApplicationContext):
        await ctx.respond("Hi, this is a global slash command from a cog!")
        
        
    # ROLE MENU        
    @commands.slash_command(description="Creates a role menu.")
    async def rolemenu(self, ctx: discord.ApplicationContext):
        await ctx.respond(
            "Self-Assignable Roles!", 
            view=RoleMenuButton()
        ) 
    
    @commands.slash_command(description="Creates an planning role button.") 
    async def shenanigans(self, ctx):
        await ctx.respond(
            "Would you like to help organize events or be involved in the club? Grab a planning role today and help us make this club better!", 
            view=ShenaniganButton()
        ) 
        
class ShenaniganButton(discord.ui.View): 
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="✨Get Involved!✨", custom_id="ShenaniganButton", style=discord.ButtonStyle.success) 
    async def button_callback(self, button, interaction:discord.Interaction):
        
        r = interaction.guild.get_role(1040769521117569074) # club revival planning committee role
        
        if r not in interaction.user.roles:
            await interaction.user.add_roles(r)
            await interaction.response.send_message(f"Gave you the planning role!", ephemeral=True, delete_after=5)
        else:
            await interaction.user.remove_roles(r)
            await interaction.response.send_message(f"Took away your planning role!", ephemeral=True, delete_after=5)


