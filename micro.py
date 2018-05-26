import discord
from discord.ext import commands
#from discord import ActivityType, Activity
import asyncio

bot = commands.Bot(command_prefix=["mm!    ","mm!   ","mm!  ","mm! ","mm!","micro ","Micro "] ,description="Micro Bot")

@bot.command()
async def hello(ctx):
    '''says hello to you'''
    await ctx.send("Hello {0}".format(ctx.message.author.mention))
@bot.command()
async def ping(ctx):
    '''pings the bot'''
    t = await ctx.send('Pong!')
    ctx.message = await ctx.channel.get_message(ctx.message.id)
    ms = (ctx.message.created_at-ctx.message.edited_at).total_seconds() * 1000
    await bot.edit_message(t, new_content='Hearing! Took: {}ms'.format(int(ms)))


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
