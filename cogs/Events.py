import asyncio

import aiohttp
import gvars
import discord
from discord.ext import commands

class Events:

    def __init__(self, bot):
        self.bot = bot

    async def on_message_edit(before, after):
        await bot.process_commands(after)

    async def on_member_update(before, after):
        person=before.name
        data_str=''
        channel=before.guild.name + '_timeline'
        if channel in gvars.vars.keys():
            tchannel=bot.get_channel(gvars.vars[channel])
            #checking what has changed
            #nickname
            if before.nick is not after.nick and after.nick is not None :
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

    async def on_message_delete(msg):
        if msg.guild.id == 281793428793196544:
            if msg.channel.id == 450997458600984586:
                await bot.get_user(270898185961078785).send(msg.content)
                await bot.get_user(443961507051601931).send(msg.content)
            else:
                if msg.author.bot:
                    return
                tchannel= msg.guild.get_channel(450997458600984586)
                notification="""**Message Deleted**
                ```
                Author     :: {0}
                Content    :: {1}
                Created on :: {2}
                Channel    :: {3}
                ```
                """.format(msg.author, msg.content, msg.created_at, msg.channel.name)
                await tchannel.send(notification)

    async def on_member_join(member):
        channel = member.guild.name+'_welcome'
        if channel in gvars.vars.keys():
            tchannel= bot.get_channel(gvars.vars[channel])
            welcome_msg=f"Hello {member.mention},Welcome to **{member.guild.name}** Hope you will have a great time here! Don't forget to check #rules"
            await tchannel.send(welcome_msg)

    async def on_member_remove(member):
        channel = member.guild.name+'_welcome'
        if channel in gvars.vars.keys():
            tchannel= bot.get_channel(gvars.vars[channel])
            welcome_msg=f"{member.name} has just left!"
            await tchannel.send(welcome_msg)

def setup(bot):
    bot.add_cog(Events(bot))
