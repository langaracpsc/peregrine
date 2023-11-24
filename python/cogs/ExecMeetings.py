import discord
from discord.ext import commands
from discord import option



class MeetingView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) 

    @discord.ui.button(label="In-Person", custom_id="meeting1", style=discord.ButtonStyle.green)
    async def in_person_button(self, button, interaction):
        # Handle when 'In-Person' button is clicked
        await self.update_attendance(interaction.user.name, "In-Person", interaction)

    @discord.ui.button(label="Online", custom_id="meetin21", style=discord.ButtonStyle.blurple)
    async def online_button(self, button, interaction):
        # Handle when 'Online' button is clicked
        await self.update_attendance(interaction.user.name, "Online", interaction)

    @discord.ui.button(label="Not Attending", custom_id="meeting3", style=discord.ButtonStyle.red)
    async def not_attending_button(self, button, interaction):
        # Handle when 'Not Attending' button is clicked
        await self.update_attendance(interaction.user.name, "Not Attending", interaction)
        
    @discord.ui.button(label="Unknown", custom_id="meeting4")
    async def unknown_button(self, button, interaction):
        # Handle when 'Not Attending' button is clicked
        await self.update_attendance(interaction.user.name, "Unknown", interaction)

    async def update_attendance(self, user, status, interaction: discord.Interaction):
        print(f"{user} marked as {status}")
        
        #print(interaction.message.embeds[0].fields)
        
        attending_users_field = interaction.message.embeds[0].fields[0]
        not_attending_users_field = interaction.message.embeds[0].fields[1]
        unknown_users_field = interaction.message.embeds[0].fields[2]
        
        auf_out:list[str] = attending_users_field.value.replace("\_", "_").split(",")
        nauf_out:list[str] = not_attending_users_field.value.replace("\_", "_").split(",")
        uuf_out:list[str] = unknown_users_field.value.replace("\_", "_").split(",")
        
        auf_out = list(map(str.strip, auf_out))
        nauf_out = list(map(str.strip, nauf_out))
        uuf_out =  list(map(str.strip, uuf_out))
        
        if auf_out[0] == "" : auf_out.pop(0)
        if nauf_out[0] == "" : nauf_out.pop(0)
        if uuf_out[0] == "" : uuf_out.pop(0)
        
        if "No one is attending yet" in auf_out: auf_out.remove("No one is attending yet")
        if "No one has declined yet" in nauf_out : nauf_out.remove ("No one has declined yet")
        
                
        if status == "Online":
            if user not in auf_out: auf_out.append(user + " (🧑)")
            
            if user in nauf_out: nauf_out.remove(user)
            if user in uuf_out: uuf_out.remove(user)
        
        elif status == "In-Person":
            if user not in auf_out: auf_out.append(user + "(🌐)")
            
            if user in nauf_out: nauf_out.remove(user)
            if user in uuf_out: uuf_out.remove(user)
        
        elif status == "Not Attending":
            if user in auf_out: auf_out.remove(user)
            
            if user not in nauf_out: nauf_out.append(user)
            
            if user in uuf_out: uuf_out.remove(user)
            
        elif status == "Unknown":
            if user in auf_out: auf_out.remove(user)
            if user in nauf_out: nauf_out.remove(user)
            if user not in uuf_out: uuf_out.append(user)
        
        interaction.message.embeds[0].set_field_at(0, name="Attending", value=", ".join(auf_out), inline=False)
        interaction.message.embeds[0].set_field_at(1, name="Not Attending", value=", ".join(nauf_out), inline=False)
        interaction.message.embeds[0].set_field_at(2, name="Unknown", value=", ".join(uuf_out), inline=False)
                
        await interaction.message.edit(embed=interaction.message.embeds[0])
        await interaction.response.edit_message(view=self) # edit the message's view
        
        #print(auf_out, nauf_out, uuf_out)
        
        
class ExecMeetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.attendance = {}  
    

    @commands.slash_command(description="Create meeting.")
    @option("date", description="Date")
    @option("time", description="Time")
    @option("meeting_num", description="Meeting number")
    @option("agenda_link", description="Agenda")
    async def meeting(self, ctx, date, time, meeting_num, agenda_link):
        
        embed = discord.Embed(
            title=f"Executive Meeting #{meeting_num}.", 
            description=f"{date} {time}\n[Agenda]({agenda_link})"
            )

        # Find the role object by name
        role = ctx.guild.get_role(798366268720676894)
        members_with_role = [member for member in ctx.guild.members if role in member.roles]
        executives = [member.name for member in members_with_role]
                    
        embed.add_field(name="Attending", value="", inline=False)
        embed.add_field(name="Not Attending", value="", inline=False)
        embed.add_field(name="Unknown", value=", ".join(executives).replace("_", "\_"), inline=False)
        
        await ctx.respond(f"Executive Meeting #{meeting_num} at {date} {time}.", embed=embed, view=MeetingView())
        return
    
def setup(bot):
    bot.add_cog(ExecMeetings(bot))
    
    
