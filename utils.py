from discord.utils import get
from discord.ext import tasks

import intervals as I
import ast

from config import (
    GUILD, 
    time_intervals, 
    saving_loop_running, 
    bot
)

def initialize_time_intervals():
    try:
        with open('TimeFinder.data', 'r') as file:
            raw_string = file.read()
        
        string_dict = ast.literal_eval(raw_string)

        converter = lambda s: datetime.strptime(s, '%H:%M').time()

        for name, string_interval in string_dict.items():
            time_intervals[name] = I.from_string(string_interval, conv = converter)

    except:
        guild = get(bot.guilds, name=GUILD)

        for member in guild.members:
            if not member.bot:
                time_intervals[member.display_name] = I.empty()

def save_time_intervals():
    store_dict = {}

    for name, interval in time_intervals.items():
        store_dict[name] = I.to_string(interval, conv = lambda v: v.strftime('%H:%M'))

    with open('TimeFinder.data', 'w+') as file:
        file.write(str(store_dict))

def time_interval_to_str(interval):
    params = {
        'disj': ', ',
        'sep': ' - ',
        'left_closed': '',
        'right_closed': '',
        'left_open': '',
        'right_open': '',
        'conv': lambda s: s.strftime('%H:%M')
    }

    return I.to_string(interval, **params)

def all_intervals_md_format(title):
    string = '```' + title + ':\n'

    for name, interval in time_intervals.items():
        string += f'\t{name}: {time_interval_to_str(interval)}\n'
    
    return string + '```'

async def send_state_in_discord(title):
    guild = get(bot.guilds, name = GUILD)
    
    role = get(guild.roles, name = 'Bot Admin')

    for member in role.members:
        if member.dm_channel is None:
            await member.create_dm()

        await member.dm_channel.send(all_intervals_md_format(title))

@tasks.loop(hours = 1)
async def keep_saving():
    save_time_intervals()
