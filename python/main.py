import discord
import os
import sys
from dotenv import load_dotenv
load_dotenv()



from bot import Peregrine

args = sys.argv
environment = None


if len(args) > 2:
    raise ValueError('Too many arguments! Enter either "dev", "prod", or nothing!')  

# DEVELOPMENT
elif len(args) == 1 or args[1].startswith("dev"):
    print("Starting the bot in development mode...")
    bot = Peregrine(token_name="DISCORD_BOT_TOKEN_DEV")
    bot.run()

# PRODUCTION
elif args[1].startswith("prod"):
    print("Starting the bot in production mode...")
    bot = Peregrine(token_name="DISCORD_BOT_TOKEN")
    bot.run()

elif args[1] == "-h":
    print("Read the source code: https://github.com/langaracpsc/peregrine")
    sys.exit(1)
    
else:
    raise ValueError(f'Unknown argument "{args[1]}".')