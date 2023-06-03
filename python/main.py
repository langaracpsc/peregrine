import discord
from discord.ext import commands
import sys
import time
from dotenv import load_dotenv
from os import environ

# Test token exists
load_dotenv()
if "DISCORD_BOT_TOKEN" not in environ:
    raise Exception("Please provide a discord bot token.")

# Initialize bot.
owner_ids:tuple[int] = (
    221780012372721664, # Highfire1#1942
    461139809583366154, # coderis.h#1684
)

bot = commands.Bot(owner_ids=owner_ids, command_prefix=commands.when_mentioned_or("?"))


# Import extensions.

extensions = (
    "cogs.Admin", 
    "cogs.CourseInfo"
    )
bot.load_extensions(*extensions)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}! (ID: {bot.user.id})\n")
    
@bot.slash_command(name="reload_extensions")    
@discord.default_permissions(administrator=True) 
async def reload_extensions(ctx: discord.ApplicationContext):
    start = time.time()
    reply = await ctx.respond(content="Reloading extensions...", ephemeral=True)
    
    for e in extensions:
        bot.unload_extension(e)
    bot.load_extensions(*extensions)
    
    end = str(time.time() - start)[:4] 
    await reply.edit_original_response(content=f"Extensions reloaded in {end} seconds.")
        
    
bot.run(environ.get("DISCORD_BOT_TOKEN"))

