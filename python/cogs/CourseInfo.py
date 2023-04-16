import discord
from discord import option
from discord.ext import commands
import os
import requests

from schema.CourseInfo import CourseInfoAll, attributes
from schema.Semester import Semester

'''
GOALS FOR FUTURE:
- split transfer information / past offerings into seperate tabs/buttons
- better formatting
'''

class CourseInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.AllCourseInfo:CourseInfoAll = CourseInfoAll.parse_file("data/allInfo.json")
        
        self.semesters = []
        for filename in os.listdir("data/json/"):
            self.semesters.append(Semester.parse_file("data/json/" + filename))
    
    # Executes code on the server
    # Not very useful tbh
    @commands.slash_command(description="Gets information for a course.")
    @option("subject", description="4 letter code of course (e.g. CPSC).")
    @option("course_code", description="4 digit code of course (e.g. 1050).")
    async def course_info(
        self, 
        ctx:discord.ApplicationContext, 
        subject:str, 
        course_code:int
        ):
        
        subject = subject.upper()
        
        find = None
        
        for c in self.AllCourseInfo.courses:
            if c.subject == subject and c.course_code == course_code:
                find = c
                break
                
        if find == None:
            await ctx.respond(f"Couldn't find information for {subject} {course_code}", ephemeral=True)
            return
        else:
            c = find
            
        embed = discord.Embed(
            title=f"{subject} {course_code} {c.title}",
            description=truncate(c.description, 4096),
            url=f"https://langara.ca/programs-and-courses/courses/{subject}/{course_code}.html",
        )
        
        embed.add_field(name="Credits:", value=c.credits)
        embed.add_field(name="Repeat limit:", value=c.rpt_limit)
        embed.add_field(name="Additional Fees:", value='${:,.2f}'.format(c.add_fees)) # format to $xx.xx
        embed.add_field(name="Availability:", value=c.availability.value)
        embed.add_field(name="Semesters offered:", value=len(c.prev_offered))
        embed.add_field(name="Last offered:", value=c.prev_offered[-1])
        
        transfer_text = []
        for t in c.transfer:
            if t.effective_end == "present":
                # use ljust for better formatting
                # invis character because discord removes excess spaces
                transfer_text.append(f"`{t.destination.ljust(5)}` {t.credit}")
        transfer_text = "\n".join(transfer_text)
        transfer_text = truncate(transfer_text, 1000)
        
        if transfer_text.isspace():
            transfer_text = "Transfer information not available."
        
        embed.add_field(name="Active transfer agreements:", value=transfer_text, inline=False)


        # i dislike this so much
        # todo: refactor c.attributes
        em = lambda s, name: f"✅ **{name}**" if c.attributes[s] else f"❌ {name}"
        
        attrs = f"{em('AR', '2AR')} {em('2SC', '2Sc')} {em('HUM', 'HUM')} {em('LSC', 'LSC')} {em('SCI', 'SCI')} {em('SOC', 'SOC')} {em('UT', 'UT')}"
       
        embed.add_field(name="Course attributes:", value=attrs, inline=False)

                
                

        embed.set_footer(text=f"Powered by data from the Langara website and bctransferguide.ca. \nData last updated {self.AllCourseInfo.datetime_retrieved}.")
        
        await ctx.respond(embed=embed)

# avoid hitting message length errors
def truncate(s:str, max_length:int, msg="\n(Truncated due to length.)") -> str:
    if len(s) < max_length:
        return s
    else:
        return s[:max_length - len(msg)] + msg

