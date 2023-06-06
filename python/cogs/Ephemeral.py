import time
import asyncio

import discord
from discord import option
from discord.ext import commands
from better_profanity import profanity

'''
Implements an ephemeral message, which deletes messages after 24 hours.

May be reworked in the future.
'''
class Ephemeral(commands.Cog):
    def __init__(self, bot:commands.Bot, 
                 ephemeral_channel=1114372341288402944, # ephemeral
                 logging_channel=1054250548762791936    # bot-development
                 ):
        self.bot = bot
        self.message_ids: list[int] = []
        
        self.channel = ephemeral_channel
        self.logging_channel = logging_channel
        
        self.color_constant = "abc"
        
        self.delete_after = 60 * 60 * 24 * 2 # 48 hours
        self.check_interval = 60*60 # check messages every hour
        
        
    async def async_init(self):
        
        channel = await self.bot.fetch_channel(self.channel)
        assert(channel != None)
        assert(channel.name == "ephemeral" or channel.name == "bot-development") # safety check
        asyncio.create_task(self.delete_old_messages())
    
    # Repeats messages sent in #ephemeral
    @commands.Cog.listener()
    @discord.default_permissions(administrator=True)
    async def on_message(self, message:discord.Message):
        if message.author.id == self.bot.application_id:
            return
        
        if message.channel.id != self.channel:
            return
        
        if message.content.strip() == "":
            return
        
        await message.delete()
                
        embed = self.generate_embed(message.content, message.author)
        message = await message.channel.send(embed=embed)
    
    # sends a message to ephemeral
    @commands.slash_command(description="Sends a message to #ephemeral")
    @option("text", description="Your message.")
    async def ephemeral(self, interaction:discord.ApplicationContext, text:str):
        
        embed = self.generate_embed(text, interaction.author)
        await self.bot.get_channel(self.channel).send(embed=embed)
        

        logging_embed = discord.Embed(
            title=f"Ephemeral message:",
            description=text,
        )
        logging_embed.set_footer(text=f"Sent by {interaction.author.name} ({interaction.author.id})",
                          icon_url=interaction.author.avatar.url)
        
        await self.bot.get_channel(self.logging_channel).send(embed=logging_embed)
        
        await interaction.respond("Sent.", ephemeral=True)
        
    # generate embed for #ephemeral
    # yes overloading author in this way isn't great but whatever
    def generate_embed(self, text:str, author:discord.User) -> discord.Embed:
        
        new_text = profanity.censor(text, censor_char="\*")
        
        color = hash(self.color_constant + author.display_name + str(author.id))
        color = color % 16777215
        
        embed = discord.Embed(
            title=f"Ephemeral message:",
            description=new_text,
            color=color
        )
        embed.set_footer(text="This message will disappear in 48 hours.")
        
        return embed

        
                
    # this code seems mildly dangerous i hope it doesn't explode
    # yes ideally you would use a sqlite database, I don't want to implement that right now
    # feel free to make a pull request
    async def delete_old_messages(self):
        
        while True:
            await asyncio.sleep(self.check_interval) # run this code every hour
            
            async for message in self.bot.get_channel(self.channel).history():
                
                # don't delete rules
                if len(message.embeds) == 1 and message.embeds[0].title == "Rules:":
                    continue
                                            
                if ( time.time() - message.created_at.timestamp() ) > self.delete_after:
                    
                    # more safety checks
                    assert(len(message.embeds) == 1 and message.embeds[0].title == "Ephemeral message:")
                    
                    await message.delete()    
        
            
             
    # sends or edits rules for #ephemeral
    @commands.slash_command(description="Sends or updates rules for #ephemeral")
    @discord.default_permissions(administrator=True)
    async def send_ephemeral_rules(self, interaction:discord.ApplicationContext):
        
        embed = discord.Embed(
            title = "Rules:",
            description = "- Messages are mirrored anonymously by <@896896783123357729>.\n- Messages in this channel delete themselves after 48 hours.\n- Message modmail if you need to delete your message.\n- Server rules still apply.",
            color = 15548997, # red
        )
        embed.set_footer(text="Like its contents, this channel may disappear in the future.")

        # search for previous rules embed
        async for message in self.bot.get_channel(self.channel).history():
            
            if message.author.id != self.bot.application_id:
                continue
                
            if len(message.embeds) == 1 and message.embeds[0].title == "Rules:":
                await message.edit(embed=embed)
                await interaction.respond("Done.", ephemeral=True)
                return
            
        await self.bot.get_channel(self.channel).send(embed=embed)
        await interaction.respond("Done.", ephemeral=True)
        
            
def setup(bot:commands.Bot):
    bot.add_cog(Ephemeral(bot))