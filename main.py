import discord
from discord.ext import commands
import time
from dotenv import load_dotenv
from os import environ

# Test that token exists.

load_dotenv()
if "DISCORD_BOT_TOKEN" not in environ:
    raise Exception("Please provide a discord bot token.")

# Initialize bot.


debug_guilds = [
    753037165050593300, # LCSC Discord Server
    714354863349170187,  # private testing server
    # 511924606651727895
]

intents = discord.Intents.default()
# intents.message_content = True
# intents.members = True

bot = commands.Bot(
    # command_prefix=commands.when_mentioned_or("?"), 
    # intents=intents,
    debug_guilds=debug_guilds
    )


# Import extensions
extensions = (
    "cogs.Admin",
    "cogs.CourseInfo",
    # "cogs.Ephemeral", # disabled due to bugginess and lack of use
    # "cogs.AntiSpam", # disabled due to non-compatibility with discord bots
    "cogs.Example",
    "cogs.Snippets"
    )
bot.load_extensions(*extensions)

# # command to initialize any async methods in cogs.
# async def async_init(bot):
#     #await bot.get_cog("Ephemeral").async_init()
#     pass
    
@bot.event
async def on_ready():    
    # Make the views persistent
    # Unfortunately, it seems like this must be done here and not in setup() in the cogs
    from cogs.Admin import AdminPanelView
    from cogs.CourseInfo import CourseView
    
    bot.add_view(AdminPanelView())
    bot.add_view(CourseView())
    
    # await async_init(bot)
    
    print(f"Logged in as {bot.user}! (ID: {bot.user.id})\n")


# Launch bot.
bot.run(environ.get("DISCORD_BOT_TOKEN"))