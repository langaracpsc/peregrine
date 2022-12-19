import discord
import os
from dotenv import load_dotenv
load_dotenv()

from RolePicker import RoleMenuButton
from EmailManager import EmailManager

guilds = [714354863349170187, 753037165050593300, 511924606651727895]
bot = discord.Bot(owner_id=221780012372721664, debug_guilds=guilds)

# ROLE MENU        
@bot.slash_command(description="Creates a role menu.")
async def rolemenu(ctx):
    await ctx.respond(
        "Self-Assignable Roles!", 
        view=RoleMenuButton()
    ) 

# PLANNING ROLE
class ShenaniganButton(discord.ui.View): 
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="✨Get Involved!✨", custom_id="ShenaniganButton", style=discord.ButtonStyle.success) 
    async def button_callback(self, button, interaction:discord.Interaction):
        
        r = interaction.guild.get_role(1040769521117569074) # club revival planning committee role
        
        if r not in interaction.user.roles:
            await interaction.user.add_roles(r)
            await interaction.response.send_message(f"Gave you the planning role!", ephemeral=True, delete_after=5)
        else:
            await interaction.user.remove_roles(r)
            await interaction.response.send_message(f"Took away your planning role!", ephemeral=True, delete_after=5)

@bot.slash_command(description="Creates an planning role button.") 
async def shenanigans(ctx):
    await ctx.respond(
        "Would you like to help organize events or be involved in the club? Grab a planning role today and help us make this club better!", 
        view=ShenaniganButton()
    ) 
    
# EMAIL VERIFICATION

class EmailModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Please enter your email.")
        self.add_item(discord.ui.InputText(label="enter your @mylangara.ca email here"))

    async def callback(self, interaction: discord.Interaction):
        email = self.children[0].value
        await email_manager.start_verification(email, interaction)
    
class VerificationCodeModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Please enter your verification code.")
        self.add_item(discord.ui.InputText(label="enter your verification code"))

    async def callback(self, interaction: discord.Interaction):
        code = self.children[0].value
        await email_manager.check_verification_code(code, interaction)


class EmailButtons(discord.ui.View): 
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Verify your email", custom_id="EmailButton", style=discord.ButtonStyle.green) 
    async def button_callback_1(self, button, interaction:discord.Interaction):
        
        if email_manager.role in interaction.user.roles:
            await interaction.response.send_message("You are already verified!", ephemeral=True)
            return
        await interaction.response.send_modal(EmailModal())

    @discord.ui.button(label="Enter your verification code", custom_id="VerificationButton", style=discord.ButtonStyle.gray) 
    async def button_callback_2(self, button, interaction:discord.Interaction):
        
        if email_manager.role in interaction.user.roles:
            await interaction.response.send_message("You are already verified!", ephemeral=True)
            return
        await interaction.response.send_modal(VerificationCodeModal())

@bot.slash_command(description="Creates an email verification menu.")
async def email_verification(ctx):
    await ctx.respond(
        "Please click here to verify your email.",
        view=EmailButtons()
    )

@bot.slash_command(description="Clear email data for a user.")
@discord.default_permissions(administrator=True)
async def clear_email_data(interaction:discord.Interaction, user_id):
    email_manager.clear_data(user_id)
    await interaction.respond(f"Cleared email data for {user_id}.", ephemeral=True)


# MISC.
@bot.slash_command(description="For benevolent dictators only.")
@discord.default_permissions(administrator=True)
async def execute(interaction:discord.Interaction, message):
    try:
        exec(message)
        await interaction.respond(f"Executed `{message}`", ephemeral=True)
    except:
        await interaction.respond("Execution failed.", ephemeral=True)
    

@bot.event
async def on_ready():
    # make buttons persistent through bot restarts
    bot.add_view(RoleMenuButton())
    bot.add_view(ShenaniganButton())
    bot.add_view(EmailButtons())
    
    # initialize email manager
    email_manager.role = bot.get_guild(753037165050593300).get_role(1054275502719914075)
    email_manager.logging = bot.get_guild(753037165050593300).get_channel(1054250548762791936)
        
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")


# no, this doesn't violate OOP at all, why do you ask?
email_manager = EmailManager("sqlite3", "database.sqlite", os.getenv("MAKE_GMAIL_WEBHOOK"))

print("Running bot!")
bot.run(os.getenv("DISCORD_TOKEN"))