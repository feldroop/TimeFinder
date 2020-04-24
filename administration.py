from discord.ext import commands

from config import (
    GUILD,
    saving_loop_running,
    time_intervals
)

from utils import (
    get,
    initialize_time_intervals,
    keep_saving,
    send_state_in_discord,
    save_time_intervals,
    I
)

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role('Bot Admin')
    @commands.command(name = 'disconnect', help = 'Disconnects the bot and saves the timetable')
    async def disconnect(self, ctx):
        await ctx.send('Goodbye.')

        await send_state_in_discord('disconnect')

        await self.bot.logout()

    @commands.Cog.listener()
    async def on_ready(self):
        guild = get(self.bot.guilds, name=GUILD)

        print(
            f'{self.bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

        initialize_time_intervals()

        global saving_loop_running
        if not saving_loop_running:
            keep_saving.start()
            saving_loop_running = True

        await send_state_in_discord('ready')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            time_intervals[member.display_name] = I.empty()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if not member.bot:
            del time_intervals[member.display_name]

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not after.bot:
            time_intervals[after.display_name] = time_intervals.pop(before.display_name)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if not after.bot:
            time_intervals[after.display_name] = time_intervals.pop(before.display_name)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        title = 'ERROR'

        if isinstance(error, commands.CheckFailure):
            await ctx.send('You are not allowed to do this.')

            title = 'CheckFailure'

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('A required argument is missing.')

            title = 'MissingRequiredArgument'

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('This command does not exist. Did you misspell it?')

            title = 'CommandNotFound'

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('You entered too many Arguments.')

            title = 'MissingRequiredArgument'

        await send_state_in_discord(title)

        # enable for debugging
        # raise error

    @commands.Cog.listener()
    async def on_disconnect(self):
        keep_saving.stop()

        save_time_intervals()
