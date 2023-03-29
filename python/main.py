import discord
import os
import sys
import requests
from dotenv import load_dotenv
load_dotenv()

from RolePicker import RoleMenuButton

bot = discord.Bot(owner_id=221780012372721664)

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
    

args = sys.argv
environment = None

# If "prod" or "dev" are passed as arguments, load dev or prod
# if no argument is provided, check for watchtower token, if present launch in prod, if not, launch in dev
if len(args) > 2:
    raise ValueError('Too many arguments! Enter either "dev", "prod", or nothing!')  

elif len(args) == 1:
    if os.getenv("WATCHTOWER_HTTP_API_TOKEN") == None:
        environment = "dev"
    else:
        environment = "prod"
  
elif len(args) == 2 and args[1] == "-h":
    print("Read the README: https://github.com/langaracpsc/peregrine")
    sys.exit(1)

elif args[1] == "dev":
    environment = "dev"

elif args[1] == "prod":
    environment = "prod"

else:
    raise ValueError(f'Unknown argument "{args[1]}".')

if environment == "dev":
    print("Starting the bot in development mode...")
    bot.run(os.getenv("DISCORD_BOT_TOKEN_DEV"))
    
elif environment == "prod":
    print("Starting the bot in production mode...")
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))
