import time
import asyncio

import discord
from discord.ext import commands
from better_profanity import profanity

'''
Detects if the same message is sent many times in a short interval and pings moderators
'''
class AntiSpam(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.recent_messages:list[str] = []
        self.warned_messages:list[str] = []
        
        self.moderation_channel = 1040768757037023292
        self.moderator_role = 753074601084583997
        
        self.stored_messages = 20
        self.trigger_warning = 5
        self.must_have_url = True
        
    
    # Listens to all messages
    @commands.Cog.listener()
    @discord.default_permissions(administrator=True)
    async def on_message(self, message:discord.Message):
        
        # ignore messages sent by bot
        if message.author.id == self.bot.application_id:
            return
        
        # ignore discord messages
        if message.content.strip() == "":
            return
        
        # don't alert unless message has a url and option enabled
        if not self.must_have_url and not 'https://' in message.content:
            return
        
        # don't alert if a moderator sends spam
        if message.author.guild_permissions.manage_messages:
            return
        
        self.recent_messages.append((message.author.id, message.content))
        
        # only save last 20 messages
        if len(self.recent_messages) > self.stored_messages:
            self.recent_messages.pop(0)
        
        # prevent memory leaks
        if len(self.warned_messages) > 100:
            self.warned_messages.pop(0)        
        
        # look for duplicated messages
        for m in self.recent_messages:
            count = 0
            
            for n in self.recent_messages:
                if m[1] == n[1]:
                    count += 1
                    
            if count >= self.trigger_warning and m[1] not in self.warned_messages:
                self.warned_messages.append(m[1])
                
                embed = discord.Embed(
                    title=f"Potential Spam Detected",
                    description=f"{m[1]}\n{message.jump_url}\n\nThis message was sent `{count}` times by <@{m[0]}>.",
                )
                embed.set_footer(text="If this isn't spam, you can safely ignore this message.")

                await self.bot.get_channel(self.moderation_channel).send(content=f"<@&{self.moderator_role}> potential spam detected!",allowed_mentions=discord.AllowedMentions(roles=True))
                await self.bot.get_channel(self.moderation_channel).send(embed=embed)
                
def setup(bot:commands.Bot):
    bot.add_cog(AntiSpam(bot))