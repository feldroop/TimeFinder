import os
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# to be eliminated when discord.py version 1.4 is available
saving_loop_running = False

time_intervals = {}

bot = commands.Bot(command_prefix='!')
