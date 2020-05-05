from discord.ext import commands

from utils import (
    time_intervals_to_str_readable,
    all_intervals_format,
    long_name,
    get_common_interval,
    build_iterator,
    is_empty
)

from queries import(
    get_time_interval,
    in_database
)

class Output(commands.Cog):
    """The commands in this command group let you view the registered and compute common time intervals."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'when')
    async def when(self, ctx, day_pattern):
        """Calculates the common time intervals of all members.
        
        This computes the intersection of the time intervals in active mode for all members of the server on the given day(s).

        Example: !when weekend"""

        iterator = build_iterator(days = day_pattern)

        output = '**Common time intervals for all members:**\n'

        for day, in iterator:
            common_interval = get_common_interval(day)

            if is_empty(common_interval):
                output += f'\t**{long_name(day)}**: No common time interval.\n'
            
            else:
                output += f'\t**{long_name(day)}**: {time_intervals_to_str_readable(common_interval)}\n'
        
        await ctx.send(output)

    @commands.command(name = 'show_all')
    async def show_all(self, ctx, mode_pattern, day_pattern):
        """Prints currently registered time intervals.
        
        Reads the database for the given mode(s) and returns a formatted version of the time intervals of all the server's users on the given day(s).
        
        Example: !show_all active weekdays"""

        iterator = build_iterator(modes = mode_pattern, days = day_pattern)
        
        output = '**All currently registered time intervals:**\n'

        for mode, day in iterator:
            output += all_intervals_format(mode, day)

        await ctx.send(output)

    @commands.command(name = 'show_me')
    async def show_me(self, ctx, mode_pattern, day_pattern):
        """Prints currently registered time intervals for the calling user.
        
        Reads the database for the given mode(s) and returns a formatted version of the time intervals of the calling user on the given day(s).
        
        Example: !show_me profile fri"""

        iterator = build_iterator(modes = mode_pattern, days = day_pattern)
        
        user_id = ctx.author.id
    	
        for mode, day in iterator:
            if day == 'mon':
                if not in_database(user_id, mode):
                    await ctx.send(f'You have no registered time intervals in {mode}.')
                    return

                output = f'**Time intervals for {ctx.author.display_name} in {mode}:**\n'

            interval = get_time_interval(user_id, day, mode)
            output += f'\t**{long_name(day)}:** {time_intervals_to_str_readable(interval)}\n'

        await ctx.send(output)
