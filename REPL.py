
from discord.ext import commands
import os
import time
import datetime
import math
import asyncio
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io
ownerid = 443961507051601931

class REPL():

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    def cleanup_code(self, content):
        'Automatically removes code blocks from the code.'
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:(- 1)])
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.command(hidden=True, name='exec')
    async def _eval(self, ctx, *, body: str):
        if ctx.author.id != ownerid:
            await ctx.send("How dare you use this command!")
            return
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result,
        }
        env.update(globals())
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')
        paginator = commands.Paginator(prefix='```py\n', suffix='\n```', max_size=2000)
        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))
        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            for line in '{}{}'.format(value, traceback.format_exc()).splitlines():
                paginator.add_line(line)
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('☑')
            except:
                pass
            if ret is None:
                if value:
                    for line in value.splitlines():
                        paginator.add_line(line)
            else:
                self._last_result = ret
                for line in ('%s%s' % (value, ret)).splitlines():
                    paginator.add_line(line)
        for page in paginator.pages:
            await ctx.send(page)

    @commands.command(hidden=True)
    async def repl(self, ctx):
        if ctx.author.id != ownerid:
            await ctx.send("How dare you use this command!")
            return
        msg = ctx.message
        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'guild': msg.guild,
            'channel': msg.channel,
            'author': msg.author,
            '_': None,
        }
        paginator = commands.Paginator(prefix='```py\n', suffix='\n```', max_size=2000)
        if msg.channel.id in self.sessions:
            await ctx.send('Already running a REPL session in this channel. Exit it with `quit`.')
            return
        self.sessions.add(msg.channel.id)
        await ctx.send('Enter code to execute or evaluate. `exit()` or `quit` to exit.')
        while True:
            response = await self.bot.wait_for('message', check=(lambda m: m.content.startswith('`') and m.author.id==ownerid and m.channel==ctx.channel))
            cleaned = self.cleanup_code(response.content)
            if cleaned in ('quit', 'exit', 'exit()'):
                await ctx.send('Exiting.')
                self.sessions.remove(msg.channel.id)
                return
            executor = exec
            if cleaned.count('\n') == 0:
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval
            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    await ctx.send(self.get_syntax_error(e))
                    continue
            variables['message'] = response
            fmt = None
            stdout = io.StringIO()
            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = '{}{}'.format(value, traceback.format_exc())
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = '{}{!r}'.format(value, result)
                    variables['_'] = result
                elif value:
                    fmt = '{}'.format(value)
            try:
                if fmt is not None:
                    for line in fmt.splitlines():
                        try:
                            paginator.add_line(line)
                        except RuntimeError:
                            splitted = [line[i:i + 1988] for i in range(0, len(line), 1988)]
                            for part in splitted:
                                paginator.add_line(part)
                    for page in paginator.pages:
                        await ctx.send(page)
                    paginator.pages.clear()
            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                await msg.channel.send('Unexpected error: `{}`'.format(e))

def setup(bot):
    bot.add_cog(REPL(bot))
