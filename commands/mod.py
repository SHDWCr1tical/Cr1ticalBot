import discord
from discord.ext import commands


class ModCog(commands.Cog, name='Moderation'):
    
    def __init__(self, client):
        self.client = client
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await self.ctx.send(f'{member.displayname} was kicked because: {reason}.')
        print('Someone was kicked from a guild.')
      
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member : discord.Member, *, reason=None):
      
        await member.send(f'You were banned because: {reason}.')
        await member.ban(reason=reason)
        await self.ctx.send(f'{member.displayname} was banned because: {reason}.')
        print('Someone was banned from a guild.')
      
    @commands.command
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, *, member):
        banned_users = await self.ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
    
        for ban_entry in banned_users:
            user = ban_entry.user
    
            if (user.name, user.discriminator) == (member_name, member_discriminator):
            await self.ctx.guild.unban(user)
            await self.ctx.send(f'Unbanned {user.name}#{user.discriminator}')
            return
      
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def stop(ctx):
        await self.ctx.channel.purge(limit=1)
        await self.ctx.send("client going offline...")
      await self.ctx.client.logout()
      print('Bot offline.!')
    
      
    @client.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount=5,):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f':ok_hand:｜{amount} message(s) deleted.')
        
def setup(client):
    client.add_cog(ModCog(client))
    print('Moderation is loaded.')