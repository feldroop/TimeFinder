from datetime import time 
from itertools import product as iter_product

from setup import (
    time_format,
    file_existed,
    datetime,
    GUILD,
    bot,
    P
)

from queries import (
    get_all_intervals,
    get_in_db_ids,
    get,
    delete_user,
    initialize_database,
    get_time_interval,
    set_time_interval,
    in_database,
    initialize_user
)

# parsing
class ParseError(Exception):
    pass 

def parse_day_pattern(day_pattern):
    day_pattern = day_pattern.lower()

    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    if day_pattern == 'all':
        return days

    elif day_pattern == 'weekend':
        return days[5:]

    elif day_pattern == 'weekdays':
        return days[:5]

    elif day_pattern in days:
        return [day_pattern]

    raise ParseError('This day pattern does not exist. Did you misspell it?')

def parse_mode_pattern(mode):
    mode = mode.lower()

    if mode == 'active' or mode == 'profile':
        return [mode]
    
    if mode == 'both':
        return ['active', 'profile']

    raise ParseError('This mode does not exist. Did you misspell it?')

def parse_time_intervals(raw_intervals):
    time_intervals = []
    
    try:
        split_intervals = map(lambda i: tuple(i.split('-')),  raw_intervals)

        for time_begin, time_end in split_intervals:
            interval = P.closed(
                datetime.strptime(time_begin, time_format).time(),
                datetime.strptime(time_end, time_format).time()
                )

            if is_empty(interval):
                time_intervals.append(f'{time_begin}-{time_end}')

            else:
                time_intervals.append(interval)

    except:
        raise ParseError("At least one of your time intervals has the wrong format. It should be XX:XX-XX:XX. No time intervals have been added.")

    return time_intervals

# formatting
def time_intervals_to_str_readable(*intervals):
    if intervals == ():
        return 'no intervals'

    params = {
        'disj': ', ',
        'sep': ' - ',
        'left_closed': '',
        'right_closed': '',
        'left_open': '',
        'right_open': '',
        'conv': lambda s: s.strftime(time_format)
    }
    output = ''

    for interval in intervals:
        if is_empty(interval):
            output += 'empty, '

        else:
            output += P.to_string(interval, **params) + ', '

    return output[:-2]

def all_intervals_format(mode, day):
    string = f'\t**{long_name(day)}:**\n'
    
    guild = get(bot.guilds, name = GUILD) 

    for user_id, interval in get_all_intervals(mode, day):
        member = get(guild.members, id = user_id)

        string += f'\t\t{member.name}: {time_intervals_to_str_readable(interval)}\n'

    return string

def long_name(day):
    mapping = {
        'mon': 'monday',
        'tue': 'tuesday',
        'wed': 'wednesday',
        'thu': 'thursday',
        'fri': 'friday',
        'sat': 'saturday',
        'sun': 'sunday',
        'weekdays': 'weekdays',
        'weekend': 'weekends', 
        'all': 'all days'     
    }

    return mapping[day.lower()]

# miscellaneous database operations
def delete_inactive_users():
    guild = get(bot.guilds, name=GUILD)

    active_ids = [member.id for member in guild.members]

    for mode in parse_mode_pattern('both'):
        in_db_ids = get_in_db_ids(mode)

        inactive_ids = list(set(in_db_ids) - set(active_ids))
        
        for user_id in inactive_ids:
            delete_user(user_id, mode)

def get_common_interval(day):
    common_interval = P.closed(time(0, 0), time(23, 59))

    all_intervals = get_all_intervals('active', day)

    for entry in all_intervals:
        common_interval &= entry[1]

    return common_interval.apply(lambda i : (P.CLOSED, i.lower, i.upper, P.CLOSED))

async def update_time_interval(command_string, ctx, mode_pattern, day_pattern, operator, raw_intervals):
    user_id = ctx.author.id

    iterator = build_iterator(modes = mode_pattern, days = day_pattern, intervals = raw_intervals)
    
    done_intervals = []

    for mode, day, interval in iterator:
        if isinstance(interval, str):
            await ctx.send(f'The time interval {interval} has been evaluated to being empty. Did you swap the begin and end time? The intervals given after this have not been added.')
            break

        done_intervals.append(interval)

        interval = operator(get_time_interval(user_id, day, mode), interval)

        set_time_interval(user_id, day, mode, interval)

    # the dict stuff is to delete duplicate entries
    output_intervals = time_intervals_to_str_readable(*dict.fromkeys(done_intervals))

    await ctx.send(f'{command_string} {output_intervals} for {ctx.author.display_name} on {long_name(day_pattern)} in {mode_pattern}.')

# miscellaneous help functions
def build_iterator(**kwargs):
    parsers = {
        'modes': parse_mode_pattern,
        'days': parse_day_pattern,
        'intervals': parse_time_intervals
    }

    iterables = []

    for category, pattern in kwargs.items():
        iterables.append(parsers[category](pattern))

    return iter_product(*iterables)

def is_empty(interval):
    return interval.apply(lambda i : (P.OPEN, i.lower, i.upper, P.OPEN)).empty
