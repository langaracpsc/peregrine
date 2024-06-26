import time
import asyncio

import discord
from discord.ext import commands
from discord.utils import get
from better_profanity import profanity

'''

Detects if the same message is sent many times in a short interval and pings moderators.



'''
class AntiSpam(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.recent_messages:list[str] = []
        self.warned_messages:list[str] = []
        
        self.moderation_channel = 1040768757037023292
        self.moderator_role = 753074601084583997
        
        self.stored_messages = 100
        self.trigger_warning = 5
        
        self.must_have_url = False
        self.hash_salt = "langara computer science club!"
        
    
    # Listens to all messages
    @commands.Cog.listener()
    @discord.default_permissions(administrator=True)
    async def on_message(self, message:discord.Message):        
        
        # ignore messages sent by bot
        if message.author.id == self.bot.application_id:
            return
        
        # ignore discord messages (e.g. "message was pinned")
        if message.content.strip() == "":
            return
        
        # don't alert unless message has a url and option enabled
        # if not self.must_have_url and not 'https://' in message.content:
        #     return
        
        # don't alert if a moderator sends spam
        # if message.author.guild_permissions.manage_messages:
        #     return
        
        msg = (message.author.id, hash(self.hash_salt + message.content))
        self.recent_messages.append(msg)
        
        # only save last 20 messages
        if len(self.recent_messages) > self.stored_messages:
            self.recent_messages.pop(0)
        
        # prevent memory leaks
        # (although this should NEVER be run because it means that we have had 100 scam alerts)
        if len(self.warned_messages) > 200:
            self.warned_messages.pop(0)        
        
        # look for duplicated messages
        for m in self.recent_messages:
            count = 0
            
            for n in self.recent_messages:
                if m[1] == n[1]:
                    count += 1
                    
            if count >= self.trigger_warning and m[1] not in self.warned_messages:
                self.warned_messages.append(m[1])
                
                # Send warning message to moderators channel.
                embed = discord.Embed(
                    title=f"Potential Spam Detected",
                    description=f"{m[1]}\n{message.jump_url}\n\nThis message was sent `{count}` times by <@{m[0]}>.",
                )
                embed.set_footer(text="If this isn't spam, then you need to remove the quarantined role from the above user.")

                await self.bot.get_channel(self.moderation_channel).send(content=f"<@&{self.moderator_role}> potential spam detected!",allowed_mentions=discord.AllowedMentions(roles=True))
                await self.bot.get_channel(self.moderation_channel).send(embed=embed)
                
                quarantine_role = message.guild.get_role(1041191067019657267)
                await message.author.add_roles(quarantine_role)
                
                
def setup(bot:commands.Bot):
    bot.add_cog(AntiSpam(bot))