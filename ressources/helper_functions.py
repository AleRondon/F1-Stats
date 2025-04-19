import logging
from datetime import timedelta
from ressources.classes.Driver import Driver
from ressources.classes.Constructor import Constructor
from ressources.database_functions_sqlite3 import get_points_by_driver_ranking_fromDB, get_points_by_constructors_ranking_fromDB,get_done_races_fromDB,get_done_sprints_fromDB,get_points_of_P1_Driver_fromDB, get_points_of_P1_Constructor_fromDB
from ressources.constants import RACE_POINTS, SPRINT_POINTS, TOTAL_RACES, TOTAL_SPRINTS, MAX_POINTS_RACE_CONSTRUCTOR, MAX_POINTS_RACE_DRIVER, MAX_POINTS_SPRINT_CONSTRUCTOR, MAX_POINTS_SPRINT_DRIVER, LOG_FILE, LOG_FORMAT

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

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

def attribute_points(position:str,session_type:str) -> int:
    points: int = 0
    if session_type == 'Race':
        points = RACE_POINTS[position]
    elif session_type == 'Sprint':
        points = SPRINT_POINTS[position]
    else:
        points = 0
    return points

def get_previous_points_driver(sql_connection,car_number:int, round_number:int) -> int:
    points: int = 0
    if round_number == 1:
        points = 0
    else:
        points = get_points_by_driver_ranking_fromDB(sql_connection,round_number-1,car_number)
    return points

def get_previous_points_constructor(sql_connection,paddock_number:int, round_number:int) -> int:
    points: int = 0
    if round_number == 1:
        points = 0
    else:
        points = get_points_by_constructors_ranking_fromDB(sql_connection,round_number-1,paddock_number)
    return points

def is_driver_championship_chance(sql_connection,points:int,round_number:int) -> bool:
    if round_number == 1:
        return True
    done_races:int = get_done_races_fromDB(sql_connection)
    done_sprints: int = get_done_sprints_fromDB(sql_connection)
    # Get points of P1
    points_p1: int = get_points_of_P1_Driver_fromDB(sql_connection,round_number)
    available_races: int = TOTAL_RACES - done_races
    available_sprints: int = TOTAL_SPRINTS - done_sprints
    available_points: int = (available_races*MAX_POINTS_RACE_DRIVER) + (available_sprints*MAX_POINTS_SPRINT_DRIVER)
    if (points+available_points) > points_p1:
        return True
    else:
        return False

def is_constructor_championship_chance(sql_connection,points:int,round_number:int) -> bool:
    if round_number == 1:
        return True
    done_races:int = get_done_races_fromDB(sql_connection)
    done_sprints: int = get_done_sprints_fromDB(sql_connection)
    # Get points of P1
    points_p1: int = get_points_of_P1_Constructor_fromDB(sql_connection,round_number)
    available_races: int = TOTAL_RACES - done_races
    available_sprints: int = TOTAL_SPRINTS - done_sprints
    available_points: int = (available_races*MAX_POINTS_RACE_CONSTRUCTOR) + (available_sprints*MAX_POINTS_SPRINT_CONSTRUCTOR)
    if (points+available_points) > points_p1:
        return True
    else:
        return False

