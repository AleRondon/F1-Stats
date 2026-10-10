import logging
from datetime import timedelta
from typing import Tuple, Dict
from ressources.classes.Driver import Driver
from ressources.classes.Constructor import Constructor
from ressources.classes.Result import Result
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
    '''Returns the points attributed to each position according to the dictionaries RACE_POINTS and SPRINT_POINTS in the constants.py file'''
    points: int = 0
    if session_type == 'Race':
        points = RACE_POINTS[position]
    elif session_type == 'Sprint':
        points = SPRINT_POINTS[position]
    else:
        points = 0
    logger.info(f'Position {position} is attributed {points} points for the session type: {session_type}.')
    return points

def get_previous_points_driver(sql_connection,car_number:int, round_number:int) -> int:
    '''Returns the number of points accumulated by a driver for the previous rounds'''
    logger.info(f'Calculating points for driver No. {car_number} before round: {round_number}')
    points: int = 0
    if round_number == 1:
        points = 0
    else:
        points = get_points_by_driver_ranking_fromDB(sql_connection,round_number-1,car_number)
    logger.info(f'Driver No. {car_number} has {points} points before round: {round_number}')
    return points

def get_previous_points_constructor(sql_connection,paddock_number:int, round_number:int) -> int:
    '''Returns the number of points accumulated by a constructor for the previous rounds'''
    logger.info(f'Calculating points for constructor No. {paddock_number} before round: {round_number}')
    points: int = 0
    if round_number == 1:
        points = 0
    else:
        points = get_points_by_constructors_ranking_fromDB(sql_connection,round_number-1,paddock_number)
    logger.info(f'Constructor No. {paddock_number} has {points} points before round: {round_number}')
    return points

def is_driver_championship_chance(sql_connection,points:int,round_number:int) -> bool:
    '''Returns if the driver has mathematical chances of winning the championship, based on the number of available races and sprints, and the points difference with current P1'''
    logger.info(f'Calculating chances for WDC with {points} by Round: {round_number}')
    if round_number == 1:
        return True
    done_races:int = get_done_races_fromDB(sql_connection)
    done_sprints: int = get_done_sprints_fromDB(sql_connection)
    points_p1: int = get_points_of_P1_Driver_fromDB(sql_connection,round_number)
    available_races: int = TOTAL_RACES - done_races
    available_sprints: int = TOTAL_SPRINTS - done_sprints
    available_points: int = (available_races*MAX_POINTS_RACE_DRIVER) + (available_sprints*MAX_POINTS_SPRINT_DRIVER)
    if (points+available_points) > points_p1:
        logger.info(f'With {points} by Round: {round_number} is still possible to win the WDC')
        return True
    else:
        logger.info(f'With {points} by Round: {round_number} is no longer possible to win the WDC')
        return False

def is_constructor_championship_chance(sql_connection,points:int,round_number:int) -> bool:
    '''Returns if the constructor has mathematical chances of winning the championship, based on the number of available races and sprints, and the points difference with current P1'''
    logger.info(f'Calculating chances for WCC with {points} by Round: {round_number}')
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
        logger.info(f'With {points} by Round: {round_number} is still possible to win the WCC')
        return True
    else:
        logger.info(f'With {points} by Round: {round_number} is no longer possible to win the WCC')
        return False

def is_not_time_result(result:str) -> bool:
    if result == 'DNS' or result == 'DNF' or result == 'DSQ':
        return True
    else:
        return False

def compare_results_H2H(driver1: Driver,driver2: Driver,results_driver1: list[Result],results_driver2: list[Result]) -> Tuple[
    Dict[str, int],
    Dict[str, int],
    Dict[str, int],
    float]:
    '''Compares the results of two drivers Head to Head, giving results by each type of session, only taking into account comparable sessions (e.g. Q1 with Q1, not Q1 and Q3).
    Returns three dictionaries: driver1 counter, driver 2 counter, comparable sessions counter, and the average delta time as a float'''
    driver1_ahead_counter: Dict[str,int] = dict()
    driver2_ahead_counter: Dict[str,int] = dict()
    comparable_sessions_counter: Dict[str,int] = dict()
    time_delta: float = 0
    time_delta_count: int = 0
    time_delta_sum: float = 0
    
    for d1 in results_driver1:
        for d2 in results_driver2:
            driver1_ahead_counter[d1.session_type] = driver1_ahead_counter.get(d1.session_type,0)
            driver2_ahead_counter[d2.session_type] = driver2_ahead_counter.get(d2.session_type,0)
            driver1_ahead_counter[d2.session_type] = driver1_ahead_counter.get(d2.session_type,0)
            driver2_ahead_counter[d1.session_type] = driver2_ahead_counter.get(d1.session_type,0)
            comparable_sessions_counter[d1.session_type] = comparable_sessions_counter.get(d1.session_type,0)
            
            #Checks that both drivers qualified for the session
            if not (hasattr(d1, 'session_type') and d1.session_type == d2.session_type and hasattr(d2, 'session_type') and d2.session_type == d1.session_type and hasattr(d1, 'round_number') and d1.round_number == d2.round_number and hasattr(d2, 'round_number') and d2.round_number == d1.round_number):
                logger.info(f'Drivers do not have common session')
                continue
            #Checks if both drivers had a DNF, DNS or DSQ
            if is_not_time_result(d1.result_time) and is_not_time_result(d2.result_time):
                logger.info(f'Both drivers had a DNF, DNS or DSQ')
                continue
            #Checks that driver 1 had a DNF, DNS or DSQ but driver 2 finished the session
            if is_not_time_result(d1.result_time) and not is_not_time_result(d2.result_time):
                logger.info(f'For round {d1.round_number} and session {d1.session_type}, {driver1.name} had a {d1.result_time}, but {driver2.name} finished with a time {d2.result_time}')
                driver2_ahead_counter[d2.session_type] = driver2_ahead_counter.get(d2.session_type,0) + 1
                comparable_sessions_counter[d1.session_type] = comparable_sessions_counter.get(d1.session_type,0) + 1
                logger.info(f'# {driver2.name} ahead #')
                continue
            #Checks that driver 2 had a DNF, DNS or DSQ but driver 1 finished the session
            if not is_not_time_result(d1.result_time) and is_not_time_result(d2.result_time):
                logger.info(f'For round {d1.round_number} and session {d1.session_type}, {driver2.name} had a {d2.result_time}, but {driver1.name} finished with a time {d1.result_time}')
                driver1_ahead_counter[d1.session_type] = driver1_ahead_counter.get(d1.session_type,0) + 1
                comparable_sessions_counter[d1.session_type] = comparable_sessions_counter.get(d1.session_type,0) + 1
                logger.info(f'# {driver1.name} ahead #')
                continue
            
            d1_result_time = float(d1.result_time)
            d2_result_time = float(d2.result_time)

            #Checks if driver 1 finished ahead of driver 2
            if int(d1.car_position) < int(d2.car_position):
                logger.info(f'For round {d1.round_number} and session {d1.session_type}, {driver1.name} finished in {d1.car_position}, while {driver2.name} finished in {d2.car_position}')
                driver1_ahead_counter[d1.session_type] = driver1_ahead_counter.get(d1.session_type,0) + 1
                comparable_sessions_counter[d1.session_type] = comparable_sessions_counter.get(d1.session_type,0) + 1
                time_delta = d1_result_time - d2_result_time
                time_delta_sum += time_delta
                time_delta_count += 1
                logger.info(f'# {driver1.name} ahead #')
                
            #Checks if driver 2 finished ahead of driver 1
            else:
                logger.info(f'For round {d1.round_number} and session {d1.session_type}, {driver1.name} finished in {d1.car_position}, while {driver2.name} finished in {d2.car_position}')
                driver2_ahead_counter[d2.session_type] = driver2_ahead_counter.get(d2.session_type,0) + 1
                comparable_sessions_counter[d1.session_type] = comparable_sessions_counter.get(d1.session_type,0) + 1
                time_delta = d1_result_time - d2_result_time
                time_delta_sum += time_delta
                time_delta_count += 1
                logger.info(f'# {driver2.name} ahead #')
                
    time_delta_average: float = time_delta_sum / time_delta_count

    return driver1_ahead_counter, driver2_ahead_counter, comparable_sessions_counter, time_delta_average