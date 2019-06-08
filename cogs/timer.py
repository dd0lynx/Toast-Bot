import os, os.path
import errno
import json
import asyncio
import discord
from discord.ext import commands, tasks

from cogs.util import file_handling as f

timers_json = 'json\\timers.json'

isYear = ['Years', 'Year', 'years', 'year', 'Y', 'y']
isDay = ['Days', 'Day', 'days', 'day', 'D', 'd']
isHour = ['Hours', 'Hour', 'hours', 'hour', 'H', 'h']
isMinute = ['Minutes', 'Minute', 'minutes', 'minute', 'M', 'm']
isSecond = ['Seconds', 'Second', 'seconds', 'second', 'S', 's']

def years_to_days(thisYear, yearsLater):
    targetYear = (thisYear + yearsLater)
    days = (targetYear * 365) + 97 * int(targetYear / 400)
    days -= (thisYear * 365) + 97 * int(thisYear / 400)
    return days

def parse_time(time):
    now = datetime.now() #time at function call
    y = 0
    d = 0
    h = 0
    m = 0
    s = 0
    print(len(time))
    print(time)
    for i in range(len(time)):
        if time[i] in isYear:
            y = int(time[i - 1])
        elif time[i] in isDay:
            d = int(time[i - 1])
        elif time[i] in isHour:
            h = int(time[i - 1])
        elif time[i] in isMinute:
            m = int(time[i - 1])
        elif time[i] in isSecond:
            s = int(time[i - 1])
    if y > 0:
        d += years_to_days(now.year(), y)
    td = timedelta(
        days=d,
        hours=h,
        minutes=m,
        seconds=s
    )
    date = now + td
    return date.strftime('%b %d %Y %I:%M%p')

def timer_calc(name, timer):
    setTime = datetime.strptime(timer['setTime'], '%b %d %Y %I:%M%p')
    timeRemaining = setTime - datetime.now()

    if datetime.now() > setTime:
        return '**{}**\nDone'.format(name)
    years = timeRemaining.days // 365.25
    days = timeRemaining.days
    hours = timeRemaining.seconds // 3600
    minutes = (timeRemaining.seconds - hours * 3600) // 60
    seconds = timeRemaining.seconds - hours * 3600 - minutes * 60

    if years > 0:
        return '**{}**\n{} years {} days {} hours {} minutes {} seconds'.format(name, years, days, hours, minutes, seconds)
    elif days > 0:
        return '**{}**\n{} days {} hours {} minutes {} seconds'.format(name, days, hours, minutes, seconds)
    elif hours > 0:
        return '**{}**\n{} hours {} minutes {} seconds'.format(name, hours, minutes, seconds)
    elif minutes > 0:
        return '**{}**\n{} minutes {} seconds'.format(name, minutes, seconds)
    else:
        return '**{}**\n{} seconds'.format(name, seconds)

class Timer(commands.Cog):

    '''commands for the creation and managment of timers running on the server'''

    def __init__(self, bot):
        self.bot = bot
        self.timers = f.load_json(timers_json)
        for guild in self.bot.guilds:
            if str(guild.id) not in self.timers:
                self.timers[str(guild.id)] = {'timers': {},
                                              'settings': {
                                                  'timer_channel': None,
                                                  'timer_message': None }}
        f.save_json(timers_json, self.timers)

    async def on_guild_join(self, ctx, guild):
        if str(guild.id) not in self.timers:
            self.timers[str(guild.id)] = {'timers': {},
                                          'settings': {
                                              'timer_channel': None,
                                              'timer_message': None }}

    @commands.group(aliases=['timers'])
    async def timer(self, ctx):
        if ctx.subcommand_passed is None:
            await ctx.send('subcommands are: [create], [remove], [list], [repost], [set]')

    @timer.command(name='create')
    async def create(self, ctx, name, *, time):
        guild = str(ctx.guild.id)
        self.timers[guild]['timers'][name] = {'set_time': parse_time(time.split())}
        f.save_json(timers_json, self.timers)

    # @_create.error()
    # async def create_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('Please enter the name of the timer, surounded in quotations if it\'s more then one word' +
    #                        'and a number followed by a length of time (years, days, minutes, etc...) in any combination' +
    #                        'ex: !timer create "end of the world" 20 years 7 days 420 hours')
    #     else:
    #         await ctx.send('An error has happened')

    @timer.command(name='remove')
    async def remove(self, ctx):
        guild = str(ctx.guild.id)
        del self.timers[guild]['timers'][name]
        f.save_json(timers_json, self.timers)

    @timer.command(name='list')
    async def list(self, ctx):
        guild = str(ctx.guild.id)
        msg = '\n'.join(timer for timer in self.timers['timers'])
        ctx.send(msg)

    @timer.command(name='repost')
    async def repost(self, ctx):
        guild = str(ctx.guild.id)
        channel_id = self.timers['settings']['timer_channel']
        timer_channel = self.bot.get_channel(int(channel_id))
        msg = await timer_channel.send("Timers go here")
        self.timers[guild]['settings']['timer_message'] = str(msg.id)
        f.save_json(timers_json, self.timers)

    @timer.group(name='set')
    async def set(self, ctx):
        if ctx.subcommand_passed is 'set':
            await ctx.send('subcommands are: <timer name> <new time>, [channel]')
        else:
            print(ctx.subcommand_passed)
            print(set.subcommands)

    @set.command(name='channel')
    async def channel(self, ctx):
        guild = str(ctx.guild.id)
        msg = await ctx.send("Timers go here")
        self.timers[guild]['settings']['timer_channel'] = str(ctx.channel.id)
        self.timers[guild]['settings']['timer_message'] = str(msg.id)
        f.save_json(timers_json, self.timers)

def setup(bot):
    bot.add_cog(Timer(bot))
