#Copyright [2021] [SHDWCr1tical]

#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

import discord
from discord.ext import commands


class ModCog(commands.Cog, name='Moderation'):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member.displayname} was kicked because: {reason}.')
        print('Someone was kicked from a guild.')
      
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member : discord.Member, *, reason=None):
      
        await member.ban(reason=reason)
        await ctx.send(f'{member.displayname} was banned because: {reason}.')
        print('Someone was banned from a guild.')
      
    @commands.command
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
    
        for ban_entry in banned_users:
            user = ban_entry.user
    
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return
      
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send("Bot going offline...")
        await ctx.Bot.logout()
        print('Bot offline.!')
    
      
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5,):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f':ok_hand:｜{amount} message(s) deleted.')
        
def setup(bot):
    bot.add_cog(ModCog(bot))
    print('Moderation is loaded.')
