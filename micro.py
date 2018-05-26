import discord
from discord.ext import commands
from discord import ActivityType, Activity
import asyncio
import os

bot = commands.Bot(command_prefix=["mm!    ","mm!   ","mm!  ","mm! ","mm!","micro ","Micro "] ,description="Micro Bot")

@bot.command()
async def hello(ctx):
    '''says hello to you'''
    await ctx.send("Hello {0}".format(ctx.message.author.mention))
@bot.command()
async def ping(ctx):
    '''pings the bot'''
    await ctx.send(':ping_pong: Pong!')

@bot.command()
async def serverinfo(ctx):
    em=discord.Embed(colour=discord.Colour(0xf1c40f))
    em.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    em.set_thumbnail(url=ctx.guild.icon_url)
    em.add_field(name="**Owner**", value=ctx.guild.owner.name)
    em.add_field(name="**Server Created on**", value=ctx.guild.created_at)
    em.add_field(name="**Member Count**", value=ctx.guild.member_count)
    em.add_field(name="**Server Emojis**", value=str(len(ctx.guild.emojis)))
    roles=ctx.guild.roles
    rolestr=''
    for role in roles:
        rolestr += role.name+','
    em.add_field(name="**Roles**" ,value=rolestr)
    await ctx.send(embed=em)

@bot.command()
async def emojis(ctx):
    emojistr=''
    emojis=ctx.guild.emojis
    if len(emojis) == 0 :
        emojistr='No Emojis available'
    else:
        for emote in emojis:
            emojistr +=' '+str(emote)+' '
    ctx.send(emojistr)
@bot.add_command(emojis)
##################################################################
@bot.event
async def on_ready():
    print("I'm ready!")
    bot.load_extension("REPL")
#@bot.event
#async def on_message(msg) :
#    if str(msg.author.id) == "443961507051601931" :
#        await bot.process_commands(msg)
messages = [
    (discord.ActivityType.watching, 'Doraemon |mm!help'),
    (discord.ActivityType.watching, 'Phineas and Ferb|mm!help'),
    (discord.ActivityType.watching, 'Timon and Pumba |mm!help'),
    (discord.ActivityType.listening, 'mm!help'),
    (discord.ActivityType.playing, 'with Uday...|mm!help'),

]

async def presence_task():
    index = -1
    while True:
        await bot.wait_until_ready()
        index = (index + 1) % len(messages)
        next_type, next_msg = messages[index]
        await bot.change_presence(activity=discord.Activity(name=next_msg, type=next_type))
        await asyncio.sleep(10)

bot.loop.create_task(presence_task())




bot.run(os.getenv('TOKEN'))
