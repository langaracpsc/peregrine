import discord
import os
import sys
from dotenv import load_dotenv
load_dotenv()


from cogs.OnboardingMenu import OnboardingMenu
from cogs.Admin import Admin

bot = discord.Bot(owner_id=221780012372721664)
bot.add_cog(OnboardingMenu(bot))
bot.add_cog(Admin(bot))

# TODO: refactor into components folder/files
from cogs.RolePicker import RoleMenuButton
from cogs.OnboardingMenu import ShenaniganButton

@bot.event
async def on_ready():
    # make buttons persistent through bot restarts
    bot.add_view(RoleMenuButton())
    bot.add_view(ShenaniganButton())

    print(f"Logged in as {bot.user}! (ID: {bot.user.id})\n")


# If "prod" or "dev" are passed as arguments, load dev or prod
# if no argument is provided, check for watchtower token, if present launch in prod, if not, launch in dev

args = sys.argv
environment = None

if len(args) > 2:
    raise ValueError('Too many arguments! Enter either "dev", "prod", or nothing!')  

elif len(args) == 1:
    if os.getenv("WATCHTOWER_HTTP_API_TOKEN") == None:
        environment = "dev"
    else:
        environment = "prod"
  
elif len(args) == 2 and args[1] == "-h":
    print("Read the source code: https://github.com/langaracpsc/peregrine")
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
    