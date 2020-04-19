import os
from dotenv import load_dotenv

import discord
from discord.ext import commands

from datetime import datetime
from datetime import time
import intervals as I

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

time_intervals = {}

def initialize_time_intervals():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    for member in guild.members:
        if not member.bot:
            time_intervals[member.name] = I.empty()

def time_interval_to_str(interval):
    params = {
        'disj': ', ',
        'sep': ' - ',
        'left_closed': '',
        'right_closed': '',
        'left_open': '',
        'right_open': '',
        'conv': lambda v: v.strftime('%H:%M')
    }

    return I.to_string(interval, **params)

def all_intervals_md_format(title):
    string = '```' + title + ':\n'

    for name, interval in time_intervals.items():
        string += f'\t{name}: {time_interval_to_str(interval)}\n'
    
    return string + '```'

async def send_state_in_discord(title):
    guild = discord.utils.get(bot.guilds, name = GUILD)
    
    role = discord.utils.get(guild.roles, name = 'Bot Admin')

    for member in role.members:
        if member.dm_channel is None:
            await member.create_dm()

        await member.dm_channel.send(all_intervals_md_format(title))

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    initialize_time_intervals()

    await send_state_in_discord('ready')

@bot.command(name='add', help='Adds a time interval, format: XX:XX XX:XX')
async def add(ctx, time_begin , time_end):
    name = ctx.author.name

    try:
        time_interval = I.closed(
            datetime.strptime(time_begin, '%H:%M').time(),
            datetime.strptime(time_end, '%H:%M').time()
            )

        time_intervals[name] |= time_interval

        await ctx.send(f'Added {time_interval_to_str(time_interval)} for {name}.')

    except:
        await ctx.send('Incorrect time format.')
    
    finally:
        await send_state_in_discord(f'add ({ctx.author.name})')

@bot.command(name='when', help='Calculates the common time of all members')
async def when(ctx):
    common_interval = I.closed(time(0, 1), time(23, 59))

    for member_interval in time_intervals.values():
        common_interval &= member_interval

    if common_interval.is_empty():
        await ctx.send('There is no common time.')
    else:
        await ctx.send(time_interval_to_str(common_interval))

    await send_state_in_discord(f'when ({ctx.author.name})')

@bot.command(name='show', help='Prints all currently registered time intervals')
async def show(ctx):
    await ctx.send(all_intervals_md_format('Time intervals'))

    await send_state_in_discord(f'show ({ctx.author.name})')

@commands.has_role('Bot Admin')
@bot.command(name='reset_all', help='Empties the timetable for everyone, only "Bot Admin" can do this')
async def reset_all(ctx):
    time_intervals.clear()

    initialize_time_intervals()

    await ctx.send('Emptied the timetable.')

    await send_state_in_discord(f'reset_all ({ctx.author.name})')

@bot.command(name='reset_me', help='Empties the timetable for the calling user')
async def reset_me(ctx):
    name = ctx.author.name

    time_intervals[name] = I.empty()

    await ctx.send(f'Emptied the timetable for {name}.')

    await send_state_in_discord(f'reset_me ({name})')

@bot.event
async def on_command_error(ctx, error):
    title = 'ERROR'

    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You are not allowed to do this')

        title = 'Permission denied'
    
    await send_state_in_discord(title)

bot.run(TOKEN)