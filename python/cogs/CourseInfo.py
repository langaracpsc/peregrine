import discord
from discord.ext import commands
import os
import requests

from schema.CourseInfo import CourseInfoAll
from schema.Semester import Semester

class CourseInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.AllCourseInfo:CourseInfoAll = CourseInfoAll.parse_file("data/")
        
        self.semesters = []
        for filename in os.listdir("data/json/"):
            self.semesters.append(Semester.parse_file("data/json/" + filename))
    
    # Executes code on the server
    # Not very useful tbh
    @commands.slash_command(description="For administrative purposes only.")
    async def course_info(self, interaction:discord.Interaction, message):
        try:
            exec(message)
            await interaction.respond(f"Executed `{message}`", ephemeral=True)
        except:
            await interaction.respond("Execution failed.", ephemeral=True)
