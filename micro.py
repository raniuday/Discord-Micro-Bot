import discord
from discord.ext import commands
from discord import ActivityType, Activity
import asyncio
import os
from datetime import datetime

bot = commands.Bot(command_prefix=["mm!    ","mm!   ","mm!  ","mm! ","mm!","micro ","Micro "] ,description="Micro Bot")
bot.launch_time = datetime.utcnow()

@bot.command()
async def uptime(ctx):
    '''Micro's uptime'''
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")

@bot.command()
async def hello(ctx):
    '''says hello to you'''
    await ctx.send("Hello {0}".format(ctx.message.author.mention))

@bot.command()
async def ping(ctx):
    '''Pong! check whether Micro is breathing or not'''
    resp = await ctx.send('Pong! Loading...')
    diff = resp.created_at - ctx.message.created_at
    await resp.edit(content=f'Pong! That took {1000 * diff.total_seconds():.1f}ms.')

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
            em.set_footer(text="Rquested by {0}".format(ctx.author.name))
            await ctx.send(embed=em)
            return
    msg=await ctx.send("Enter a valid role.\n Make sure that you enter **name** of the role but don`t mention it.")
    await asyncio.sleep(4)
    msg.delete()
    return



##################################################################
@bot.event
async def on_message_edit(before, after):
  await bot.process_commands(after)

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
        if after.guild.id == 446649726578720778:    #Micro`s birth place
            tchannel=after.guild.get_channel(450134437691392011)
        elif after.guild.id == 281793428793196544:   #IU United
            tchannel=after.guild.get_channel(450341762536308736)
        #checking what has changed
        #nickname
        if before.nick is not after.nick and after.nick != None :
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
            if tchannel == 450341762536308736 :
                data_str="**{0}** has changed Profile Picture".format(person)
                pfp_embed=discord.Embed(title=data_str,colour=discord.Colour(0x3498db))
                pfp_embed.set_author(name=person,icon_url=after.avatar_url)
                pfp_embed.set_image(url=after.avatar_url)
                await tchannel.send(embed=pfp_embed)
@bot.event
async def on_message_delete(msg):
    if msg.author.bot :
        return
    if msg.guild.id == 281793428793196544 :
        tchannel= msg.guild.get_channel(450997458600984586)
        desc=msg.content
        em=discord.Embed(title="Message Delete detected in {0}".format(msg.channel.name))
        em.add_field(name="Author:",value=msg.author)
        em.add_field(name="Content of deleted message",value=desc)
        em.add_field(name="Created on:",value=msg.created_at)
        await tchannel.send(embed=em)

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
