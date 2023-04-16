import discord
import os
from dotenv import load_dotenv
load_dotenv()


class Peregrine:
    def __init__(self, token_name:str):
        self.owner_ids:tuple[int] = (
            221780012372721664, # Highfire1#1942
        )
        self.token_name = token_name
        
    def run(self):
    
        bot = discord.Bot(owner_ids=self.owner_ids)
        
        # add cogs
                
        from cogs.OnboardingMenu import OnboardingMenu
        from cogs.Admin import Admin
        from cogs.CourseInfo import CourseInfo
        bot.add_cog(OnboardingMenu(bot))
        bot.add_cog(Admin(bot))
        bot.add_cog(CourseInfo(bot))

        # TODO: refactor into components folder/files
        from cogs.RolePicker import RoleMenuButton
        from cogs.OnboardingMenu import ShenaniganButton

        @bot.event
        async def on_ready():
            # make buttons persistent through bot restarts
            bot.add_view(RoleMenuButton())
            bot.add_view(ShenaniganButton())

            print(f"Logged in as {bot.user}! (ID: {bot.user.id})\n")
            
            
        
        bot.run(os.getenv(self.token_name))