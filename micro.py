import discord
from discord.ext import commands
from discord import ActivityType, Activity
import asyncio
import os
from datetime import datetime
import gvars

bot = commands.Bot(command_prefix=["mm!    ","mm!   ","mm!  ","mm! ","mm!","micro ","Micro "] ,description="Micro Bot")
bot.launch_time = datetime.utcnow()

@bot.command()
async def uptime(ctx):
    '''Micro's uptime'''
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"Micro is online since {days}d, {hours}h, {minutes}m, {seconds}s")

@bot.command()
async def hello(ctx):
    '''says hello to you'''
    await ctx.send("Hello {0}".format(ctx.message.author.mention))

@bot.command()
async def ping(ctx):
    '''Pong! check whether Micro is breathing or not'''
    resp = await ctx.send('Pong! Loading...')
    diff = resp.created_at - ctx.message.created_at
    await resp.edit(content=f':champagne: Cheers! That took {1000 * diff.total_seconds():.1f}ms.')

@bot.command()
async def serverinfo(ctx):
    '''current server info '''
    em=discord.Embed(colour=discord.Colour(0xf1c40f))
    em.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
    em.set_thumbnail(url=ctx.guild.icon_url)
    em.add_field(name="**Owner**", value=ctx.guild.owner.name)
    em.add_field(name="**Server Created on**", value=ctx.guild.created_at)
    em.add_field(name="**Member Count**", value=ctx.guild.member_count)
    em.add_field(name="**Server Emojis**", value=str(len(ctx.guild.emojis)))
    em.add_field(name="**You joined on **",value=str(ctx.author.joined_at))
    roles=ctx.guild.roles
    rolestr=''
    for role in roles:
        rolestr += role.name+','
    em.add_field(name="**Roles**" ,value=rolestr)
    await ctx.send(embed=em)

@bot.command()
async def emojis(ctx):
    """Display the current server's local emojis"""
    emojistr=''
    emojis=ctx.guild.emojis
    if len(emojis) == 0 :
        emojistr='No Emojis available'
    else:
        for emote in emojis:
            emojistr +=' '+str(emote)+' '
    await ctx.send(emojistr)
@bot.command()
async def feedback(ctx,*,message : str):
    '''Give your feedback on Micro'''
    tchannel=bot.get_guild(446649726578720778).get_channel(450297549006307329)
    server=ctx.guild.name
    channel=ctx.channel
    em_title='{0} on "{1}->{2}" said:'.format(ctx.author,server,channel)
    em=discord.Embed(title=em_title, description=message,colour=discord.Colour(0x992d22))
    await tchannel.send(embed=em)
@bot.command()
async def rolelist(ctx,*,role_name):
    '''Displays the members with specified role.
    To avoid unnecessary mentions, this command only takes name, mention wouldn`t work.'''
    for role in ctx.guild.roles:
        if role.name.lower() == role_name.lower() :
            member_list = role.members
            em=discord.Embed(title='Member(s) with {0} role in this server'.format(role.name))
            em.colour = role.colour
            emoji= ':diamond_shape_with_a_dot_inside:'
            members=''
            for member in member_list:
                members += emoji+member.name+'\n'
            if len(members)> 2048:
                await ctx.send("Sorry! {0} names can`t fit here".format(str(len(member_list))))
                return
            em.description = members
            em.set_footer(text="Requested by {0}".format(ctx.author.name))
            await ctx.send(embed=em)
            return
    msg=await ctx.send("Enter a valid role.\n Make sure that you enter **name** of the role but don`t mention it.")
    await asyncio.sleep(4)
    msg.delete()
    return



##################################################################

@bot.event
async def on_ready():
    extensions=('REPL','Admin','Events')
    for i in extensions:
        try:
            bot.load_extension(f"cogs.{i}")
        except Exception as e:
            await bot.get_channel(449863094290612224).send(f"Error Loading {i}\n ```py {str(e)}```")
    print("I'm ready!")
    await bot.get_channel(449863094290612224).send(f"Bot reawakened at {datetime.now(): %B %d, %Y at %H:%M:%S GMT}")


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
