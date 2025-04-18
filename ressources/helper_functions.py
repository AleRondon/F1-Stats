from datetime import timedelta

from ressources.classes.Driver import Driver
from ressources.classes.Constructor import Constructor
from ressources.variables import RACE_POINTS, SPRINT_POINTS

def convert_time_to_seconds(time_string:str) -> float:
    """
    Convert a time string in format 'h:mm:ss.ss' or 'm:ss.ss' into seconds as a float.
    :param time_string: str - the time string to be converted, e.g., "1:42:06.304" or "1:15.096"
    :return: float - the total number of seconds represented by the input string
    """

    # Try parsing as hours, minutes, and seconds first
    try:
        h, m, s = map(float, time_string.split(':'))
        if h > 0:
            hours = timedelta(hours=h)
            minutes = timedelta(minutes=m)
            seconds = timedelta(seconds=s)

            total_seconds = hours.total_seconds() + minutes.total_seconds() + seconds.total_seconds()
        else:
            raise ValueError("Invalid time string format")
    except ValueError:
        # If parsing as hours, minutes, and seconds fails, try parsing as minutes and seconds only
        try:
            m, s = map(float, time_string.split(':', 1))
            if m > 0:
                minutes = timedelta(minutes=m)
                seconds = timedelta(seconds=s)

                total_seconds = minutes.total_seconds() + seconds.total_seconds()
            else:
                raise ValueError("Invalid time string format")
        except ValueError:
            # If parsing as minutes and seconds only fails, try parsing as seconds alone
            try:
                s = float(time_string)
                if s >= 0.0:
                    total_seconds = s
                else:
                    raise ValueError("Invalid time string format")
            except ValueError:
                raise ValueError("Driver did not finished the session")

    return total_seconds

def get_driver_by_number(sql_connection,car_number:int) -> Driver:
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''Select name, trigramme, nationality from Drivers where car_number = ?''',(car_number,))
    name:str = sql_cursor.fetchone()[0]
    trigramme:str = sql_cursor.fetchone()[1]
    nationality:str = sql_cursor.fetchone()[2]
    driver:Driver = Driver(name,trigramme,car_number,nationality)
    return driver

def get_driver_by_trigramme(sql_connection,trigramme:str) -> Driver:
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''Select name, car_number, nationality from Drivers where trigramme = ?''',(trigramme,))
    name:str = sql_cursor.fetchone()[0]
    car_number:int = int(sql_cursor.fetchone()[1])
    nationality:str = sql_cursor.fetchone()[2]
    driver:Driver = Driver(name,trigramme,car_number,nationality)
    return driver

def get_constructor_by_number(sql_connection,paddock_number:int) -> Constructor:
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''Select full_name,result_name,short_name from Constructor where paddock_number = ?''',(paddock_number,))
    full_name:str = sql_cursor.fetchone()[0]
    result_name:str = sql_cursor.fetchone()[1]
    short_name:str = sql_cursor.fetchone()[2]
    constructor:Constructor = Constructor(full_name,result_name,short_name,paddock_number)
    return constructor

def get_constructor_by_name(sql_connection,result_name:str) -> Constructor:
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''Select full_name,paddock_number,short_name from Constructor where result_name = ?''',(result_name,))
    full_name:str = sql_cursor.fetchone()[0]
    paddock_number:int = int(sql_cursor.fetchone()[1])
    short_name:str = sql_cursor.fetchone()[2]
    constructor:Constructor = Constructor(full_name,result_name,short_name,paddock_number)
    return constructor

def attribute_points(position:str,session_type:str) -> int:
    points: int = 0
    if session_type == 'Race':
        points = RACE_POINTS[position]
    elif session_type == 'Sprint':
        points = SPRINT_POINTS[position]
    else:
        points = 0
    return points