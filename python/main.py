import discord
import sys
from dotenv import load_dotenv
from os import environ

# Test token exists
load_dotenv()
if "DISCORD_BOT_TOKEN" not in environ:
    raise Exception("Please provide a discord bot token.")

# Initialize bot
owner_ids:tuple[int] = (
    221780012372721664, # Highfire1#1942
)
bot = discord.Bot(owner_ids=owner_ids)


# add cogs
    
from cogs.OnboardingMenu import OnboardingMenu
from cogs.Admin import Admin
from cogs.CourseInfo import CourseInfo

bot.add_cog(OnboardingMenu(bot))
bot.add_cog(Admin(bot))
bot.add_cog(CourseInfo(bot))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}! (ID: {bot.user.id})\n")
    
    

bot.run(environ.get("DISCORD_BOT_TOKEN"))