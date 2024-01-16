import discord
from discord.ext import commands
import sys
import time
from dotenv import load_dotenv
from os import environ

# Test that token exists.

load_dotenv()
if "DISCORD_BOT_TOKEN" not in environ:
    raise Exception("Please provide a discord bot token.")

# Initialize bot.

owner_ids:tuple[int] = (
    221780012372721664, # Highfire1#1942
    461139809583366154, # coderis.h#1684
)

debug_guilds = [753037165050593300]  # Add your desired guild IDs here

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    owner_ids=owner_ids, 
    command_prefix=commands.when_mentioned_or("?"), 
    intents=intents,
    debug_guilds=debug_guilds
    )

# Import extensions.

extensions = (
    "cogs.Admin", 
    # "cogs.CourseInfo", # disabled right now due to outdated implementation
    # "cogs.Ephemeral", # disabled due to bugginess and lack of use
    "cogs.AntiSpam",
    "cogs.Misc",
    "cogs.ExecMeetings"
    )
bot.load_extensions(*extensions)


# command to initialize any async methods in cogs.
async def async_init(bot):
    #await bot.get_cog("Ephemeral").async_init()
    pass
    
# Log when bot starts
@bot.event
async def on_ready():
    await async_init(bot)
    
    # make buttons persistent through bot restarts
    # why can't i do this in setup() ??????
    from cogs.ExecMeetings import MeetingView
    
    from cogs.Admin import AdminPanelView
    

    bot.add_view(MeetingView())
    bot.add_view(AdminPanelView())
    
    print(f"Logged in as {bot.user}! (ID: {bot.user.id})\n")
    
    
# Command to reload extensions.

@bot.slash_command(name="reload_extensions")    
@discord.default_permissions(administrator=True) 
async def reload_extensions(ctx: discord.ApplicationContext, specific_cog:str = None):
    start = time.time()
    reply = await ctx.respond(content="Reloading extensions...", ephemeral=True)
    
    reload = extensions
    if specific_cog != None:
        reload = (specific_cog)
    
    reply_msg = ""
    
    for e in reload:
        try:
            bot.reload_extension(e)
        except Exception as e:
            reply_msg += str(e) + "\n\n"
            
    await async_init(bot)
    
    end = str(time.time() - start)[:4] 
    reply_msg += f"Extensions reloaded in {end} seconds."
    await reply.edit_original_response(content=reply_msg)
    
async def reload_all_extensions() -> int:
    for e in extensions:
        bot.reload_extension(e)
       
    await async_init(bot)
    return len(extensions)
        
# Launch bot.

bot.run(environ.get("DISCORD_BOT_TOKEN"))