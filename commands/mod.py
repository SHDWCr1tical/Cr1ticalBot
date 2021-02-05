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
