import discord
from discord.ext import commands, tasks
from bot import initial_extensions
from cogs.util.file_handling import load_cog, unload_cog

class Admin(commands.Cog):

    '''Bot commands for you, the deveolper'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='logout', hidden=True, aliases=['exit', 'close', 'stop', 'die'])
    @commands.is_owner()
    async def _logout(self, ctx):
        '''stops bot'''
        await self.bot.close()

    @commands.command(name='test1')
    @commands.is_owner()
    async def _test1(self, ctx):
        ctx.send('boop')

    @commands.command(name='test2')
    async def _test2(self, ctx):
        ctx.send('boop2')

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog):
        print('load called')
        if load_cog(self.bot, cog):
            if cog not in initial_extensions:
                initial_extensions.append(cog)

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def _unload(self, ctx, *, cog):
        print('unload called')
        if unload_cog(self.bot, cog):
            if cog in initial_extensions:
                initial_extensions.remove(cog)

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog=None):
        print('reload called')
        if cog:
            unload_cog(self.bot, cog)
            load_cog(self.bot, cog)
        else:
            for extension in initial_extensions:
                unload_cog(self.bot, extension)
                load_cog(self.bot, extension)

def setup(bot):
    bot.add_cog(Admin(bot))
