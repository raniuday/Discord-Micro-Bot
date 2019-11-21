import asyncio

import aiohttp
import discord
from discord.ext import commands


class Admin(commands.Cog):
    '''For administrative purposes'''

    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member):
        '''Kick members from your server'''
        try:
            await member.kick()
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member):
        '''Ban toxic members from your server'''
        try:
            await member.ban()
            await ctx.message.add_reaction('\u2705')
        except:
            await ctx.message.add_reaction('\u274C')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, number: int):
        '''Clears specified number of messages, ranging from 2 to 100'''
        await ctx.channel.purge(limit=number)

def setup(bot):
    bot.add_cog(Admin(bot))
