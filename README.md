# TimeFinder

A discord bot to find common available times for meetings.

## Usage

### Prerequisites

Apart from a discord account and running server you will need Python 3 (.6.9+) and the following packages:

```
discord.py (1.3.3)
python-dotenv (0.13.0)
python-intervals (1.10.0.post1)
```

It might also run on older/newer versions of the above software.

### Installing

* Create a bot for your server/guild at discordapp.com/developers. 
* Clone this this repository and add a .env file with the following content:

```
TOKEN={your-bot's-token}
GUILD={your-server/guild's-name}
```

### Run

Run `TimeFinder.py` with your Python 3 distribution. It should connect to your server, where you can find out more about the command interface by typing `!help`. 

If you give yourself the role "Bot Admin" on your server, you will get direct messages about the internal state of the program every time someone enters a command. This feature exists mainly for debugging purposes.

## Contributing

I work on this project mainly for fun and don't expect any contributions. But if you like the bot and want to add a feature, don't hesitate to make a pull request!

## Acknowledgments

* Great guide I used for this project: https://realpython.com/how-to-make-a-discord-bot-python/.
* You could just use Doodle or something like that.
