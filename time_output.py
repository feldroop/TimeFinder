from discord.ext import commands

from datetime import time

from utils import (
    time_intervals,
    time_interval_to_str,
    send_state_in_discord,
    all_intervals_md_format,
    I
)
class Output(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'when', help = 'Calculates the common time of all members')
    async def when(self, ctx):
        common_interval = I.closed(time(0, 1), time(23, 59))

        for member_interval in time_intervals.values():
            common_interval &= member_interval

        if common_interval.is_empty():
            await ctx.send('There is no common time.')
        else:
            await ctx.send(time_interval_to_str(common_interval))

        await send_state_in_discord(f'when ({ctx.author.display_name})')

    @commands.command(name = 'show', help = 'Prints all currently registered time intervals')
    async def show(self, ctx):
        await ctx.send(all_intervals_md_format('Time intervals'))

        await send_state_in_discord(f'show ({ctx.author.name})')
