from setup import (
    db_connection,
    db_cursor,
    TOKEN, 
    bot,
    time_interval_from_str,
    P
)

from time_input import Input
from time_output import Output
from administration import Administration
from usage import Usage

def main():
    bot.add_cog(Input(bot))
    bot.add_cog(Output(bot))
    bot.add_cog(Administration(bot))
    bot.add_cog(Usage(bot))

    bot.run(TOKEN)

    db_cursor.close()
    db_connection.close()

if __name__ == "__main__":
    main()
