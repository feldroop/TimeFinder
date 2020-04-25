from discord.ext import commands
from datetime import datetime

from utils import (
    send_state_in_discord,
    time_interval_to_str,
    initialize_time_intervals,
    get,
    I
)

from config import (
    time_intervals,
    GUILD
)

class Input(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'add', help = 'Adds a time interval, format: XX:XX XX:XX')
    async def add(self, ctx, time_begin, time_end):
        name = ctx.author.display_name

        try:
            time_interval = I.open(
                datetime.strptime(time_begin, '%H:%M').time(),
                datetime.strptime(time_end, '%H:%M').time()
                )

        except:
            await ctx.send('Incorrect time format.')
        
        
        if time_interval.is_empty():
            await ctx.send('Your time interval is empty. Did you swap the begin and end time?')

        else:
            try: 
                time_intervals[ctx.author.id] |= time_interval

                await ctx.send(f'Added {time_interval_to_str(time_interval)} for {name}.')
            
            except:
                await ctx.send('Insertion failed. Try full reseting if possible.')

        await send_state_in_discord(f'add ({name})')

    @commands.has_role('Bot Admin')
    @commands.command(name = 'reset_all', help = 'Resets the timetable for everyone to the last saved state, only "Bot Admin" can do this')
    async def reset_all(self, ctx):
        time_intervals.clear()

        initialize_time_intervals()

        await ctx.send('Reseted the timetable.')

        await send_state_in_discord(f'reset_all ({ctx.author.display_name})')

    @commands.has_role('Bot Admin')
    @commands.command(name = 'empty', help = 'Empties the timetable for everyone, only "Bot Admin" can do this')
    async def empty(self, ctx):
        time_intervals.clear()

        guild = get(self.bot.guilds, name=GUILD)

        for member in guild.members:
            if not member.bot:
                time_intervals[member.id] = I.empty()

        await ctx.send('Emptied the timetable.')

        await send_state_in_discord(f'empty ({ctx.author.display_name})')

    @commands.command(name = 'empty_me', help = 'Empties the timetable for the calling user')
    async def empty_me(self, ctx):
        name = ctx.author.display_name

        time_intervals[ctx.author.id] = I.empty()

        await ctx.send(f'Emptied the timetable for {name}.')

        await send_state_in_discord(f'reset_me ({name})')
