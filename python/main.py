import discord
import os
import requests
from dotenv import load_dotenv
load_dotenv()

from RolePicker import RoleMenuButton

debug_guilds = [714354863349170187, 753037165050593300, 511924606651727895]
bot = discord.Bot(owner_id=221780012372721664, debug_guilds=debug_guilds)

# ROLE MENU        
@bot.slash_command(description="Creates a role menu.")
async def rolemenu(ctx):
    await ctx.respond(
        "Self-Assignable Roles!", 
        view=RoleMenuButton()
    ) 

# PLANNING ROLE
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

@bot.slash_command(description="Creates an planning role button.") 
async def shenanigans(ctx):
    await ctx.respond(
        "Would you like to help organize events or be involved in the club? Grab a planning role today and help us make this club better!", 
        view=ShenaniganButton()
    ) 

# MISC.
@bot.slash_command(description="For administrative purposes only.")
@discord.default_permissions(administrator=True)
async def execute(interaction:discord.Interaction, message):
    try:
        exec(message)
        await interaction.respond(f"Executed `{message}`", ephemeral=True)
    except:
        await interaction.respond("Execution failed.", ephemeral=True)

@bot.slash_command(description="Updates docker containers if an update exists")
@discord.default_permissions(administrator=True)
async def update_docker(interaction:discord.Interaction):
    if os.getenv("WATCHTOWER_HTTP_API_TOKEN") == None:
        await interaction.respond("No watchtower token present.", ephemeral=True)
    else:
        try:
            url     = 'http://watchtower:8080/v1/update'
            headers = {"Authorization": f"Bearer {os.getenv('WATCHTOWER_HTTP_API_TOKEN')}"}
            # go in this order so that the message actually makes it to discord
            requests.post(url)
            await interaction.respond("Update request sent to the cloud.")
            await requests.post(url, headers=headers)
        except Exception as e:
            await interaction.respond("Could not establish a connection: " + str(e))
        

@bot.event
async def on_ready():
    # make buttons persistent through bot restarts
    bot.add_view(RoleMenuButton())
    bot.add_view(ShenaniganButton())

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

print("Running bot!")
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
