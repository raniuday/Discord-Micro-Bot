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
    '''server info '''
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
    """Display local emojis"""
    emojistr=''
    emojis=ctx.guild.emojis
    if len(emojis) == 0 :
        emojistr='No Emojis available'
    else:
        for emote in emojis:
            emojistr +=' '+str(emote)+' '
    await ctx.send(emojistr)


##################################################################
@bot.event
async def on_ready():
    print("I'm ready!")
    bot.load_extension("REPL")
@bot.event
async def on_member_update(before, after):
    person=before.name
    data_str=''
    #Restricting Guilds
    if after.guild.id == 446649726578720778 or after.guild.id ==  281793428793196544:
        
        #Retrieving channel to post update
        if after.guild.id == 446649726578720778:
            tchannel=after.guild.get_channel(450134437691392011)
        elif after.guild.id == 281793428793196544:
            tchannel=after.guild.get_channel(398515843102670852)
        #checking what has changed
        #nickname
        if before.nick is not after.nick:
            data_str="Next time, when you see {1}, its our {0}".format(person,after.nick)
            nick_embed=discord.Embed(title=data_str,colour=discord.Colour(0x3498db))
            nick_embed.set_author(name=person,icon_url=after.avatar_url)
            await tchannel.send(embed=nick_embed)

        #roles
        if len(after.roles) > len(before.roles):
            added_roles=[i.name for i in after.roles if i not in before.roles]
            data_str="{0} has got ".format(person)
            for i in added_roles:
                data_str += i
            if len(added_roles)>1:
                data_str += " roles"
            else:
                data_str += " role"
            role_embed=discord.Embed(title=data_str,colour=discord.Colour(0x3498db))
            role_embed.set_author(name=person,icon_url=after.avatar_url)
            await tchannel.send(embed=role_embed)
        #Profile picture
        if before.avatar != after.avatar:
            data_str="**{0}** has changed Profile Picture".format(person)
            pfp_embed=discord.Embed(title=data_str,colour=discord.Colour(0x3498db))
            pfp_embed.set_author(name=person,icon_url=after.avatar_url)
            pfp_embed.set_image(url=after.avatar_url)
            await tchannel.send(embed=pfp_embed) 
        
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
