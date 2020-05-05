from discord.ext import commands

from setup import (
    file_existed,
    db_connection
)

from utils import (
    delete_inactive_users,
    ParseError
)

from queries import (
    initialize_database,
    delete_user,
    in_database
)

class Administration(commands.Cog):
    """The commands in this command group are for admin use only."""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role('Bot Admin')
    @commands.command(name = 'disconnect')
    async def disconnect(self, ctx):
        """Disconnects the bot.

        There are no parameters. The database is saved."""
        
        await ctx.send('Goodbye.')

        await self.bot.logout()

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f'{self.bot.user} is connected and ready.'
        )
        
        if not file_existed:
            initialize_database()
        
        else:
            delete_inactive_users()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        for mode in ['active', 'profile']: 
            if in_database(member.id, mode):
                delete_user(member.id, mode)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('You are not allowed to do this.')

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('A required argument is missing.')

        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('This command does not exist. Did you misspell it?')

        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('You entered too many Arguments.')
        
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if isinstance(original, ParseError):
                await ctx.send(original)

        # enable for debugging
        raise error
