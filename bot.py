import sys
import json
import logging
import traceback
import asyncio
import discord
from discord.ext import commands

import config

description = '''Hello! I am a basic bot'''

log = logging.getLogger(__name__)

initial_extensions = [
    'cogs.admin',
    'cogs.mtg',
    'cogs.reactions',
    'cogs.timer'
]

def load_cog(bot, cog):
    try:
        bot.load_extension(cog)
        print(f'Loaded extension {cog}.')
        return True
    except Exception as e:
        print(f'Failed to load extension {cog}.', file=sys.stderr)
        traceback.print_exc()
        return False

def unload_cog(bot, cog):
    try:
        bot.unload_extension(cog)
        print(f'Unloaded extension {cog}.')
        return True
    except Exception as e:
        print(f'Failed to unload extension {cog}.', file=sys.stderr)
        traceback.print_exc()
        return False

class Toast(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('!'),
            description=description
        )

        self.client_id = config.client_id

        for extension in initial_extensions:
            load_cog(self, extension)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry. This command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
                traceback.print_tb(original.__traceback__)
                print(f'{original.__class__.__name__}: {original}', file=sys.stderr)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(error)

    async def on_ready(self):
        print(f'Ready: {self.user} (ID: {self.user.id})')

    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        super().run(config.token, reconnect=True)
