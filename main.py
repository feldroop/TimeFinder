from config import TOKEN, bot

from time_input import Input
from time_output import Output
from administration import Administration

def main():
    bot.add_cog(Input(bot))
    bot.add_cog(Output(bot))
    bot.add_cog(Administration(bot))

    bot.run(TOKEN)

if __name__ == "__main__":
    main()