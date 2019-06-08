import requests
import asyncio
import discord
from discord.ext import commands

import config

api_url = 'https://api.imgur.com/3/'
auth_token_url = 'https://api.imgur.com/oauth2/token'

class Reactions(commands.Cog):

    '''Interactive gif commands for users, uses imgur'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def punch(self, ctx, member=None):
        await ctx.send('feature not implemented yet')

    @commands.command()
    async def poke(self, ctx, member=None):
        await ctx.send('feature not implemented yet')

    @commands.command()
    async def hug(self, ctx, member=None):
        await ctx.send('feature not implemented yet')

def setup(bot):
    bot.add_cog(Reactions(bot))
