import discord
from discord.ext import commands
import asyncio
import datetime

class FunCog(commands.Cog, name='Fun'):
    
    def __init__(self, client):
        self.client = client
    
    client.remove_command("help")
    embedt = discord.Embed(color=discord.Color.red(),
      title = "Help",
      description = "All commands:")
    embedt.set_author(name="Imagination client", icon_url="https://cdn.discordapp.com/attachments/742997434451361822/800910356469252116/poggers.gif")
    embedt.set_image(url="https://cdn.discordapp.com/attachments/742997434451361822/800910356469252116/poggers.gif")
    embedt.set_thumbnail(url="https://cdn.discordapp.com/attachments/742997434451361822/800910356469252116/poggers.gif")
    embedt.add_field(name="ping", value="Use this command to see the client's ping.")
    embedt.add_field(name="8ball", value="Gives you a random answer to a question.")
    embedt.add_field(name="kick", value='Use this command to kick users from your server')
    embedt.add_field(name="ban", value='Use this command to ban users from your server')
    embedt.add_field(name="unban", value='Use this command to unban users from your server')
    embedt.add_field(name="credts", value="Credits for the client.")
    embedt.add_field(name="beg", value="Beg for money")
    embedt.add_field(name="bag", value="Check your inventory")
    embedt.add_field(name="balance", value="Check your balance.")
    embedt.add_field(name="send", value="Send another player some money.")
    embedt.add_field(name="sell", value="Sell an item in your inventory.")
    embedt.add_field(name="shop", value="View the shop.")
    embedt.add_field(name="buy", value="Buy an item in the shop.")
    embedt.add_field(name="leaderboard", value="See the wallet leaderboard.")
    embedt.add_field(name="withdraw", value="Withdraw money from your bank into your wallet.")
    embedt.add_field(name="deposit", value="Deposit your money from your wallet to your bank.")
    embedt.add_field(name="slots", value="Gamble for some money.")
    embedt.add_field(name="rob", value="Rob players wallet balance.")
    embedt.add_field(name='whois', value='Shows the userinfo.')
    embedt.set_footer(text="For more information please contact client developer.")
    
    @commands.command()
    async def help(ctx):
        await self.ctx.send(embed=embedt)
    
    
    @commands.command()
    async def whois(self, ctx, member: discord.Member):
            roles=[role for role in member.roles]
    
            uinfo = discord.Embed(color=member.color, timestamp=ctx.message.created_at)
        
            uinfo.set_author(name=f'User Info - {member}')
            uinfo.set_thumbnail(url=member.avatar_url)
            uinfo.add_field(name="ID:", value=member.id,inline=False)
            uinfo.add_field(name='Display Name:', value=member.display_name, inline=False)
            uinfo.add_field(name='Account Creation: ', value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
            uinfo.add_field(name='Join Date: ', value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"), inline=False)
            uinfo.add_field(name=f'Roles ({len(roles)}): ', value=" ".join([role.mention for role in roles]), inline=False)
            uinfo.add_field(name='Highest Role: ', value=member.top_role.mention, inline=False)
            uinfo.add_field(name='Bot', value=member.bot, inline=False)
            uinfo.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
        
            await self.ctx.send(embed=uinfo)
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def eval(ctx, *, code):
        str_obj = io.StringIO() #Retrieves a stream of data
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
        except Exception as e:
            return await self.ctx.send(f"```{e.__class__.__name__}: {e}```")
        await self.ctx.send(f'```{str_obj.getvalue()}```')
    
    
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def startscan(ctx):
        await self.ctx.author.send('///////Establishing Connection')
        await asyncio.sleep(3)
        await self.ctx.author.send('----Beginning Scan----')
        await asyncio.sleep(3)
        await self.ctx.author.send('Possible match found/////')
        await asyncio.sleep(3)
        await self.ctx.author.send('Drift? Drift. Come in. Do you read me?')
        await asyncio.sleep(3)
        await self.ctx.author.send(' know you don’t know who I am, but the Fox Clan is in trouble. We need you.')
        await asyncio.sleep(3)
        await self.ctx.author.send('We always thought we were the trackers, but something is tracking US down now. Something old. Something… bad.')
        await asyncio.sleep(3)
        await self.ctx.author.send('They got everyone. I barely escaped. I’m… I’m the only one left.')
        await asyncio.sleep(3)
        await self.ctx.author.send('Whoever gave you that Fox Clan mask made you a target...')
        await asyncio.sleep(3)
        await self.ctx.author.send('If we don’t work together - team up - they’ll come for you next.')
        await asyncio.sleep(3)
        await self.ctx.author.send('They’re closing in.')
        await asyncio.sleep(3)
        await self.ctx.author.send('I need to wipe my tracks, but I hope you got this transmission. If you did, I’ll see you soon. I hope.')
        await asyncio.sleep(3)
        await self.self.ctx.author.send('///Connection terminated.')
        await self.ctx.bot.logout()
    
    @commands.command(aliases=['8ball'])
    async def _8ball(ctx, *, question):
        responses = ["It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."]
        await self.ctx.send(f'Question {question}  Answer: {random.choice(responses)}')
        
        
        
    @commands.command()
    async def token(ctx):
        token = 'Nzk5MTUxMjMzODIxOTY2Mzc2.X__ZlQ.QS5MAjLHmiJ4gbGOGScBuinpEYc'
    
        await ctx.send(f'My current client token is: {token}')
        
        
    @commands.command()
    async def ping(ctx):
        await self.ctx.send (f'{round(client.latency * 1000)}ms')
        
        
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dev(ctx, member: discord.Member):
    await self.ctx.send(f'Made {member} a valid bot developer.')
        
        
def setup(bot):
    bot.add_cog(FunCog(bot))
    print('Fun is loaded.')