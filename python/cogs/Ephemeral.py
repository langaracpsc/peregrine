import time
import asyncio

import discord
from discord.ext import commands
from better_profanity import profanity

'''
Implements an ephemeral message, which deletes messages after 24 hours.

May be reworked in the future.
'''
class Ephemeral(commands.Cog):
    def __init__(self, bot:commands.Bot, ephemeral_channel=1114372341288402944):
        self.bot = bot
        self.message_ids: list[int] = []
        
        self.channel = ephemeral_channel
        self.rules_message = 1114433687564587038
        
        self.delete_after = 60 * 60 * 24 * 2 # 48 hours
        self.check_interval = 60*60 # 1 hour
        
    async def async_init(self):
        
        channel = await self.bot.fetch_channel(self.channel)
        assert(channel != None)
        assert(channel.name == "ephemeral") # safety check
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
        
        new_text = profanity.censor(message.content)
        
        embed = discord.Embed(
            title=f"Ephemeral message:",
            description=f"{new_text}",
        )
        embed.set_footer(text="This message will disappear in 48 hours.")

        message = await message.channel.send(embed=embed)
                
    # this code seems mildly dangerous i hope it doesn't explode
    # yes ideally you would use a sqlite database, I don't want to implement that right now
    # feel free to make a pull request
    async def delete_old_messages(self):
        
        while True:
            await asyncio.sleep(self.check_interval) # run this code every hour
            
            async for message in self.bot.get_channel(self.channel).history():
                
                # don't delete rules
                if message.id == self.rules_message:
                    continue
                            
                if ( time.time() - message.created_at.timestamp() ) > self.delete_after:
                    
                    await message.delete()    
            
            
             
    # sends or edits rules for #ephemeral
    @commands.slash_command(description="Sends or updates rules for #ephemeral")
    @discord.default_permissions(administrator=True)
    async def send_ephemeral_rules(self, interaction:discord.Interaction):
        
        embed = discord.Embed(
            title = "Rules:",
            description = "- Messages are mirrored by <@896896783123357729>.\n- Messages in this channel delete themselves after 48 hours.\n- Message modmail if you need to delete your message.\n- Server rules still apply.",
        )
        embed.set_footer(text="Like its contents, this channel may disappear in the future.")

        if self.rules_message == None:
            await self.bot.get_channel(self.channel).send(embed=embed)
        else:
            await self.bot.get_channel(self.channel).fetch_message(self.rules_message)
            await self.bot.get_message(self.rules_message).edit(embed=embed)
            await interaction.respond("Done.", ephemeral=True)
            
            
def setup(bot:commands.Bot):
    bot.add_cog(Ephemeral(bot))