import discord
from discord.ext import commands, tasks
import random
import os
import asyncio

os.chdir('./')

mainshop = [{"name":"Watch","price":500,"description":"Time"},
            {"name":"Laptop","price":5000, "description":"Work"},
            {"name":"Desktop","price":10000,"description":"Gaming"},
            {"name":"Rifle","price":20000,"description":"Hunting"}]


client = commands.client(command_prefix = '>')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter all required arguements.')
    if isinstance(error, commands.CommandNotFound):
        print("Error occoured! Command Not Found!")
        await ctx.send("Command not found. Please try again")

@client.event
async def on_ready():
    await client.change_presence(statuses)
    print('Logged in as:')
    print(client.user.name)
    print('---------------')
    
    
async def ch_pr():
    await client.wait_untill_ready()
    
    statuses = ["activity=discord.Game(name='with the ban hammer.'))", "activity=discord.Activity(type=discord.ActivityType.watching, name='{len(client.guilds)} severs!'), 'activity=discord.Activity(type=discord.ActivityType.listening, name="to the moderation team")', 'activity=discord.Game(name="the help command.")']
    
    while not client.is_closed():
        
        status = random.choice(statuses)
        
        await client.change_presence(status)
        
        await asyncio.sleep(10)


@client.command()
async def credits(ctx):
    await ctx.send("Thanks to `Code With Swastk` for his tutorials on YouTube")
    await ctx.send("Coded by: from Cr1tical import localidiot#1393")

client.loop.create_task(ch_pr())
client.run(EDIT THIS AND PUT YOUR TOKEN)
print('Please edit this file and put your bot token to the above line in the code.')
