from discord.ext import commands
from operator import or_, sub

from utils import (
    time_intervals_to_str_readable,
    long_name,
    build_iterator,
    update_time_interval
)

from queries import (
    delete_user,
    delete_all,
    in_database,
    empty_user,
    empty_all,
    get_time_interval,
    set_time_interval
)

class Input(commands.Cog):
    """The commands in this command group modify your registered time intervals."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'add')
    async def add(self, ctx, mode_pattern, day_pattern, *time_intervals):
        """Adds one or more time intervals for the calling user
        
        It is possible to enter an arbitrary number of time intervals. The format of the time intervals has to be XX:XX-XX:XX.
        
        Example: !add profile all 10:00-12:00 17:00-20:00"""

        await update_time_interval('Added', ctx, mode_pattern, day_pattern, or_, time_intervals)

    @commands.command(name = 'remove')
    async def remove(self, ctx, mode_pattern, day_pattern, *raw_intervals):
        """Removes one or more time intervals for the calling user

        It is possible to enter an arbitrary number of time intervals. The format of the time intervals has to be XX:XX-XX:XX.
        
        Example: !remove active thu 13:00-14:00 17:00-18:00"""

        await update_time_interval('Removed', ctx, mode_pattern, day_pattern, sub, raw_intervals)

    @commands.has_role('Bot Admin')
    @commands.command(name = 'delete_all')
    async def delete_all(self, ctx, mode_pattern):
        """Deletes all database entries
        
        This should be used with a lot of caution. There is no way to retract the deleted entries.
        
        Example: !delete_all active"""

        iterator = build_iterator(modes = mode_pattern)

        for mode, in iterator:
            delete_all(mode)

        await ctx.send(f'Emptied the database for {mode}.')

    @commands.command(name = 'delete_me')
    async def delete_me(self, ctx, mode_pattern):
        """Deletes the calling user from the database
        
        This should be used with a lot of caution. There is no way to retract your deleted entry.
        
        Example: !delete_me active"""
        iterator = build_iterator(modes = mode_pattern)

        for mode, in iterator:
            delete_user(ctx.author.id, mode)

        await ctx.send(f'Deleted the user {ctx.author.display_name} from {mode_pattern}.')

    @commands.has_role('Bot Admin')
    @commands.command(name = 'empty_all')
    async def empty_all(self, ctx, mode_pattern, day_pattern):
        """Empties time intervals of all users
        
        This can be used to reset everything, but be careful. There is no way to retract the deleted information.
        
        Example: !empty_all active weekdays"""

        iterator = build_iterator(modes = mode_pattern, days = day_pattern)
        
        for mode, day in iterator:
            empty_all(mode, day)

        await ctx.send(f'Emptied the time intervals for everyone on {long_name(day_pattern)} in {mode_pattern}.')

    @commands.command(name = 'empty_me')
    async def empty_me(self, ctx, mode_pattern, day_pattern):
        """Empties the time intervals of the calling user
        
        This can be used to reset your time intervals on certain days, but be careful. There is no way to retract the deleted information.
        
        Example: !empty_me active weekdays"""
        iterator = build_iterator(modes = mode_pattern, days = day_pattern)

        for mode, day in iterator:
            empty_user(ctx.author.id, mode, day)

        await ctx.send(f'Emptied time intervals of {ctx.author.display_name} on {long_name(day_pattern)} in {mode_pattern}.')

    @commands.command(name = 'to_profile')
    async def to_profile(self, ctx, day_pattern):
        """Sets the time intervals of the calling user to his/her profile
        
        After this call, the time intervals in active, which are used to compute common time intervals, are set to equal the ones in profile. Be careful, the time intervals in active cannot be restored.
        
        Example: !to_profile all"""
        
        iterator = build_iterator(days = day_pattern)

        user_id = ctx.author.id

        if not in_database(user_id, 'profile'):
            await ctx.send('You have no registered times in profile.')
            return

        for day, in iterator:
            interval = get_time_interval(user_id, day, 'profile')
            
            set_time_interval(user_id, day, 'active', interval)

        await ctx.send(f'Set the time intervals for {ctx.author.display_name} on {long_name(day_pattern)} to his/her profile.')
