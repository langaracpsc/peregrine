import discord
from discord.ext import commands
from datetime import datetime


# All cog commands are placed into a class
class Snippets(commands.Cog):
    # Required boilerplate for all cogs
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.slash_command(description="Information about submitting volunteer hours")
    @discord.option("override_due_date", description="e.g. 14th, 21st")
    async def submit_volunteer_hours(self, ctx: discord.ApplicationContext, override_due_date=None):
        
        month = datetime.now().strftime('%B')
        
        embed = discord.Embed(
            title=f":fire: It's time to log {month} volunteer hours! :fire:"
        )     
        
        due = "7th"
        if override_due_date:
            due = override_due_date
        
        embed.description = f"""
        It's time to log volunteer hours!
        
        1) Finalize your hours on the Google Sheet: (https://docs.google.com/spreadsheets/d/1BI6hxSHRNDqEwMgLOu5b0QTtqRjhXWmQBhiFe2Tte88/edit).
        If your name is on the `Total Hours` list more than once, then that means that some of the volunteer entries associated with your name is missing information.
        
        2) Log your hours on MyImpact: (https://app.betterimpact.com/Login/LoginNoSearch?agencyGuid=45d74ffa-8b70-4924-8737-a815d5645f54)
        
        **Please submit your hours to MyImpact by {month} {due}.**
        
        Please react with a :white_check_mark: once this is completed.
        Questions? Please see the [volunteer hours document on Notion](https://www.notion.so/langaracs/Volunteer-Hour-Rules-and-Guidelines-dfb638ac0b01471580f6ea8943727284?pvs=4).
        """
        
        embed.set_image(url="https://i.ibb.co/Lxmf8wf/Untitled.png")
                    
        message = await ctx.respond(embed=embed)
        msg = await message.original_response()
        await msg.add_reaction("✅")
            
# More boilerplate
def setup(bot:commands.Bot):
    bot.add_cog(Snippets(bot))