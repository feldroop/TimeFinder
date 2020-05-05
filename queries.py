from discord.utils import get

from setup import (
    time_format,
    db_connection,
    db_cursor,
    bot,
    GUILD,
    file_existed,
    P
)

# initializers
def initialize_database():
    with db_connection:
        for mode in ['active', 'profile']:
            db_cursor.execute(f"""CREATE TABLE {mode} (
                                id INTEGER PRIMARY KEY,
                                mon INTERVAL,
                                tue INTERVAL,
                                wed INTERVAL,
                                thu INTERVAL,
                                fri INTERVAL,
                                sat INTERVAL, 
                                sun INTERVAL
                                )""")

def initialize_user(user_id, mode):
    params = {
        'id': user_id,
        'mon': P.empty(),
        'tue': P.empty(),
        'wed': P.empty(),
        'thu': P.empty(),
        'fri': P.empty(),
        'sat': P.empty(),
        'sun': P.empty()
    }

    with db_connection:
        db_cursor.execute(f"""INSERT INTO {mode}
                              VALUES (:id, :mon, :tue, :wed, :thu, :fri, :sat, :sun)""", params)

# erasers
def delete_user(user_id, mode):
    params = {'id': user_id}
    with db_connection:
        db_cursor.execute(f"""DELETE FROM {mode}
                              WHERE id = :id""", params)

def delete_all(mode):
    with db_connection:
        db_cursor.execute(f"""DELETE FROM {mode}""")

def empty_user(user_id, mode, day):
    if not in_database(user_id, mode):
        initialize_user(user_id, mode)

    else:
        params = {'id': user_id, 'interval': P.empty()}
        with db_connection:
            db_cursor.execute(f"""UPDATE {mode}
                                SET {day} = :interval
                                WHERE id = :id""", params)

def empty_all(mode, day):
    params = {'interval': P.empty()}
    with db_connection:
        db_cursor.execute(f"""UPDATE {mode}
                              SET {day} = :interval""", params)

# readers
def in_database(user_id, mode):
    params = {'id': user_id}
    db_cursor.execute(f"""SELECT * 
                          FROM {mode}
                          WHERE id = :id""", params)
    
    return not db_cursor.fetchone() is None

def get_in_db_ids(mode):
    db_cursor.execute(f"""SELECT id
                          FROM {mode}""")

    return map(lambda t: t[0], db_cursor.fetchall())

def get_all_intervals(mode, day):
    db_cursor.execute(f"""SELECT id, {day}
                          FROM {mode}""")

    return db_cursor.fetchall()

def get_time_interval(user_id, day, mode):
    if not in_database(user_id, mode):
        initialize_user(user_id, mode)

    params = {'id': user_id}

    db_cursor.execute(f"""SELECT {day}
                          FROM {mode}
                          WHERE id = :id""", params)

    return db_cursor.fetchone()[0]

# writers
def set_time_interval(user_id, day, mode, interval):
    if not in_database(user_id, mode):
        initialize_user(user_id, mode)
    
    params = {'id': user_id, 'interval': interval}

    with db_connection:
        db_cursor.execute(f"""UPDATE {mode}
                              SET {day} = :interval
                              WHERE id = :id""", params)
