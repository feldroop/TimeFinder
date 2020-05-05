from discord.ext import commands

class Usage(commands.Cog):
    """The commands in this command group help you in learning to use this bot."""
    def __init__(self, bot):
        self.bot = bot
        self.name = "help name"

    @commands.command(name = 'patterns')
    async def patterns(self, ctx):
        """Gives information about the command parameter patterns
        
        Most commands of this bot are used with certain patterns for their parameters. 
        Here you can find a list of those and what they mean."""

        await ctx.send(
            """```Most commands of this bot are used with certain patterns for their parameters. 
Here you can find a list of those and what they mean.

Pattern for time Input:

The format for entering time intervals is XX:XX-XX:XX. Make sure not to us any space characters inside the format.
Example: 14:45-16:15

Mode pattern:

This pattern describes which tables your command modifies and reads from. For more information see !tutorial.

\tactive: active table
\tprofile: profile table
\tboth: both tables

Day pattern:

This pattern describes which days of the week are referred to by your command either for in- or output.

\tmon/tue/wed/thu/fri/sat/sun: one single day (self-explanatory)
\tweekdays: mon, tue, wed thu and fri
\tweekend: sat and sun
\tall: all days
```""")

    @commands.command(name = 'tutorial')
    async def tutorial(self, ctx):
        """Gives information about hot to use this bot
        
        This is a guide on the intended usage of this bot."""

        await ctx.send("""```How to use this bot:

General Idea:

All members of a discord server register time intervals to indicate when they are available. 
You can modify these intervals with !add and !remove. Afterwards these intervals can be displayed with !show_me or !show_all. Common available time intervals are computed with !when. 

The whole bot operates over the range of one week, from monday to sunday. Therefore it is a timetable more than a calendar.

Modes:

There are two modes, profile and active. You can enter the time intervals where you are normally available into profile. These time intervals shouldn't be changed too often. You can copy these intervals to the active mode via the !to_profile command. 

The !when command operates exclusively on the time intervals registered in active. Therefore you can edit your active time intervals whenever an irregular events leads to you being available more or less during this certain week. Afterwars you can call !to_profile again and reset the changes you made for the next week.

Command usage:

Almost all command have to be called with certain patterns as parameters. See !patterns for details.

```""")