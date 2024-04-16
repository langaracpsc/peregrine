import discord
from discord import option
from discord.ext import commands, pages

import Levenshtein

import asyncio
import requests
import json
import re

'''
GOALS FOR FUTURE:
- split transfer information / past offerings into seperate tabs/buttons
- better formatting

# TODO: comment this better
'''

class CourseInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
            
    def setup(bot):
        bot.add_command(CourseInfo)
        
    # Call API
    async def getCourseFromAPI(subject:str, course_code:int) -> requests.Response:
        API_URL = "https://api2.langaracs.tech/data/"
        
        result = await asyncio.to_thread(requests.get, f"{API_URL}{subject}/{course_code}")
        return result
    
    # Create a base template embed - since this is reused it deserves its own function.
    def createBaseEmbed(subject: str, course_code: int, data:dict) -> discord.Embed:        
        embed = discord.Embed(
            title=f"{subject} {course_code} {data['courseInfo']['title']}",
            url=f"https://langara.ca/programs-and-courses/courses/{subject}/{course_code}.html"
        )     
            
        embed.set_footer(text=f"Powered by the Langara Course API. Pull requests welcome.")
        return embed
    
    def createSummaryEmbed(subject: str, course_code: int, data:dict) -> discord.Embed:
        
        c = data["courseInfo"]
        
        embed = CourseInfo.createBaseEmbed(subject, course_code, data)
        
        embed.description = "No description found.",
        if c['description'] != None:
            embed.description = c['description']

        
        embed.add_field(name="Credits:", value=c["credits"])
        
        # embed.add_field(name="Repeat limit:", value=c["rpt_limit"])
        # embed.add_field(name="Additional Fees:", value='${:,.2f}'.format(c["add_fees"])) # format to $xx.xx
        # embed.add_field(name="Availability:", value=avail)
        # embed.add_field(name="Semesters offered:", value=len(c.prev_offered))
        
        last_offered = data["offerings"][-1]
        embed.add_field(name="Last offered:", value=f"{last_offered['year']} {last_offered['term']}")
        
        # Parse attributes here as well
        
        return embed
    
    def createTransfersEmbed(subject: str, course_code: int, data:dict) -> discord.Embed:
        
        embed = CourseInfo.createBaseEmbed(subject, course_code, data)
        
        bold = ["SFU", "UBCV"]
        transfers_cleaned = []
        
        # 0 "CPSC"
        # 1	1050
        # 2	"LANG"
        # 3	"AU"
        # 4	"AU COMP 2XX (3)"
        # 5	"May/15"
        # 6	"present"
        
        # put sfu and ubc transfers first on the list
        for t in data["transfers"]:
            if t[3] in bold:
                transfers_cleaned.append(f"{t[3].ljust(4)}\u1CBC⭐ {t[4]}")
        
        if len(transfers_cleaned) > 0:
            transfers_cleaned.append("")
        
        for t in data["transfers"]:
            
            # don't show non-current transfer agreements
            if t[6] != "present":
                continue
            
            if t[3] in bold:
                continue
            
            # funny regex to get the number of credits the transfer is worth
            elif float(re.findall(r"([0-9]*)", t[4].split('(')[-1])[0]) != float(data["courseInfo"]["credits"]):
                transfers_cleaned.append(f"{t[3].ljust(4)}\u1CBC⚠️ {t[4]}")
            else:
                transfers_cleaned.append(f"{t[3].ljust(4)}\u1CBC➖ {t[4]}")
        
        final_text = "\n".join(transfers_cleaned)
        
        if final_text.isspace():
            final_text = "Transfer information not available."
        
        embed.add_field(name="Active transfer agreements:", value=f"```{final_text}```", inline=False)
        return embed
    
    def numToSemester(i:int) -> str:
        if i==10:
            return "Spring"
        if i==20:
            return "Summer"
        if i==30:
            return "Fall"
    
    def createOfferingsEmbed(subject: str, course_code: int, data:dict) -> discord.Embed:
        embed:discord.Embed = CourseInfo.createBaseEmbed(subject, course_code, data)
        
        semesters = {}
        semesters_c = {}
        
        total_offered = 0
        
        # bad and evil side effects
        data["offerings"].reverse()
        
        for o in data["offerings"]:
            
            if f'{o["year"]}{o["term"]}' not in semesters:
                semesters[f'{o["year"]}{o["term"]}'] = 0
                semesters_c[f'{o["year"]}{o["term"]}'] = 0
                
            semesters[f'{o["year"]}{o["term"]}'] += 1
            total_offered += 1
            
            if o["seats"] == "Cancel":
                semesters_c[f'{o["year"]}{o["term"]}'] += 1
        
        out1 = []
        out2 = []
        out3 = []
        year_shown = []
                
        numToEmoji = lambda i: "🌱" if int(i) == 10 else ("☀️" if int(i) == 20 else "🍂")
        numToSemester = lambda i: "Spring" if int(i) == 10 else ("Summer" if int(i) == 20 else "Fall")

        for o in semesters:
            year = int(o[0:4])
            current = None
                        
            if year >= 2020:
                current = out1
            elif year >= 2015:
                current = out2  
            elif year >= 2010:
                current = out3
            
            if current != None:
                if year not in year_shown:
                    current.append(str(year) + ":")
                    year_shown.append(year)
                
                s = f"{numToEmoji(o[4:])}: {semesters[o]} sections"
                if semesters[o] == 1:
                    s = s[:-1]
                current.append(s)
                
                if str(o) in semesters_c and semesters_c[o] > 0:
                    current.append(f" ({semesters_c[str(o)]} cancelled)")
            
        out1 = "\n".join(out1)
        out2 = "\n".join(out2)
        out3 = "\n".join(out3)
        
        print(semesters_c)
        
        embed.description = "**Previous Offerings:**"
        
        # We could have 4000 chars if we use the embed description instead of a field, but thats too much text
        if (out1 != ""):
            embed.add_field(name="2020 - now:", value=f"```{out1}```", inline=True)
        if (out2 != ""):
            embed.add_field(name="2015 - 2019:", value=f"```{out2}```", inline=True)
        if (out3 != ""):
            embed.add_field(name="2010 - 2014:", value=f"```{out3}```", inline=True)
        
        embed.add_field(name="", value="", inline=False)
        
        fo = list(semesters.keys())[-1]
        lo = list(semesters.keys())[0]
        
        embed.add_field(name="First offered:", value=f"{fo[:4]} {numToSemester(fo[4:])}", inline=True)
        embed.add_field(name="Last offered:", value=f"{lo[:4]} {numToSemester(lo[4:])}", inline=True)
        embed.add_field(name="Total sections:", value=f"{total_offered}", inline=True)
        return embed
    
    
    @commands.slash_command(description="Gets information for a course.")
    @option("subject", description="4 letter code of course (e.g. CPSC).")
    @option("course_code", description="4 digit code of course (e.g. 1050).")
    @option("verbose", description="Whether to print transfer/attributes/availability information.")
    async def course_info_testing(
        self, 
        ctx:discord.ApplicationContext, 
        subject:str, 
        course_code:int,
        verbose:bool=True
        ):
        
        # Get and parse API response
        response: requests.Response = await CourseInfo.getCourseFromAPI(subject, course_code)
        
        if response.status_code == 404:
            await ctx.respond(f"Could not find {subject} {course_code}.", ephemeral=True)
            return
        
        if response.status_code != 200:
            await ctx.respond(f"API Error: {response}", ephemeral=True)
            return
        
        data:dict = json.loads(response.content)
        
        # Parse correct embed
        embed = CourseInfo.createSummaryEmbed(subject, course_code, data)

        await ctx.respond(embed=embed, view=CourseView())

class CourseView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 
        
    def parseInfoFromEmbed(self, embed:discord.Embed) -> dict:
        title = embed.title.split()
        out = {
            "subject" : title[0],
            "course_code" : title[1],
            "page" : "info"
        }
        
        if "transfer" in str(embed.description).lower():
            out["page"] = "transfer"
        elif "previous" in str(embed.description).lower():
            out["page"] = "previous"

        return out
        

    @discord.ui.button(label="Info", custom_id="CI_0", style=discord.ButtonStyle.gray)
    async def course_info(self, button, interaction:discord.Interaction):
        
        # TODO: REFACTOR THIS HORRIBLENESS
        current_page = self.parseInfoFromEmbed(interaction.message.embeds[0])
        response: requests.Response = await CourseInfo.getCourseFromAPI(current_page["subject"], current_page["course_code"])
        if response.status_code != 200:
            await interaction.respond(f"API Error: {response}", ephemeral=True)
            return
        data:dict = json.loads(response.content)
        # END OF HORRIBLENESS
        
        embed = CourseInfo.createSummaryEmbed(current_page["subject"], current_page["course_code"], data)
        
        await interaction.message.edit(embed=embed)
        await interaction.response.defer()
    
    
    @discord.ui.button(label="Transfers", custom_id="CI_1", style=discord.ButtonStyle.gray)
    async def transfers(self, button:discord.Button, interaction:discord.Interaction):
        
        # TODO: REFACTOR THIS HORRIBLENESS
        current_page = self.parseInfoFromEmbed(interaction.message.embeds[0])
        response: requests.Response = await CourseInfo.getCourseFromAPI(current_page["subject"], current_page["course_code"])
        if response.status_code != 200:
            await interaction.respond(f"API Error: {response}", ephemeral=True)
            return
        data:dict = json.loads(response.content)
        # END OF HORRIBLENESS
        
        embed = CourseInfo.createTransfersEmbed(current_page["subject"], current_page["course_code"], data)
        
        await interaction.message.edit(embed=embed)
        await interaction.response.defer()
        
    
    @discord.ui.button(label="Offerings", custom_id="CI_2", style=discord.ButtonStyle.gray)
    async def offerings(self, button:discord.Button, interaction:discord.Interaction):
        
        # TODO: REFACTOR THIS HORRIBLENESS
        current_page = self.parseInfoFromEmbed(interaction.message.embeds[0])
        response: requests.Response = await CourseInfo.getCourseFromAPI(current_page["subject"], current_page["course_code"])
        if response.status_code != 200:
            await interaction.respond(f"API Error: {response}", ephemeral=True)
            return
        data:dict = json.loads(response.content)
        # END OF HORRIBLENESS
        
        embed = CourseInfo.createOfferingsEmbed(current_page["subject"], current_page["course_code"], data)
        
        await interaction.message.edit(embed=embed)
        await interaction.response.defer()

        
def setup(bot:commands.Bot):
    bot.add_cog(CourseInfo(bot))