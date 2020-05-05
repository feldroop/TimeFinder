import sqlite3

from os import getenv, path
from dotenv import load_dotenv

from discord.ext import commands

from datetime import datetime
import portion as P

time_format = '%H:%M'

# setup database for handling intervals
def time_interval_to_str(interval):
    converter = lambda t: t.strftime(time_format)
    temp_interval = interval.apply(lambda i : (P.CLOSED, i.lower, i.upper, P.CLOSED))
    return P.to_string(temp_interval, conv = converter)

def time_interval_from_str(bytes_string):
    converter = lambda s: datetime.strptime(s, time_format).time()
    return P.from_string(bytes_string.decode("utf-8"), conv = converter)

sqlite3.register_adapter(P.Interval, time_interval_to_str)
sqlite3.register_converter("INTERVAL", time_interval_from_str)

# connect to database
file_existed = path.isfile('TimeFinder.db')

db_connection = sqlite3.connect('TimeFinder.db', detect_types = sqlite3.PARSE_DECLTYPES)
db_cursor = db_connection.cursor()

# load data for connecting for discord
load_dotenv()

TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')
