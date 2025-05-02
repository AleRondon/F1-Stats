import sqlite3
import logging
import os
import csv
import statistics
from typing import Any, Dict
from ressources.classes.Driver import Driver
from ressources.classes.Constructor import Constructor
from ressources.classes.Round import Round
from ressources.classes.Result import Result
from ressources.classes.DriverRanking import DriverRanking
from ressources.classes.ConstructorRanking import ConstructorRanking
from ressources.helper_functions import convert_time_to_seconds, attribute_points, is_driver_championship_chance, is_constructor_championship_chance,get_previous_points_driver,get_previous_points_constructor
from ressources.database_functions_sqlite3 import initialize_db,get_constructor_by_resultname_fromDB, mark_round_done_toDB, get_all_drivers_carnumber_fromDB,get_all_constructors_paddocknumber_fromDB,get_points_by_driver_round_fromDB,get_points_by_constructors_round_fromDB, get_driver_by_trigramme_fromDB,get_last_round_fromDB, get_quali_results_by_driver_fromDB
from ressources.constants import LOG_FILE, LOG_FORMAT, DRIVERS_FILE, DRIVERS_COLUMNS, CONSTRUCTORS_FILE, CONSTRUCTORS_COLUMNS, ROUNDS_FILE, ROUNDS_COLUMNS, RESULTS_FOLDER, RESULTS_COLUMNS

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

def check_and_initialize_db(filename:str) -> sqlite3.Connection:
    """Check if DATABASE_FILE exists, and call initialize_db() if it doesn't."""

    if not os.path.isfile(filename):  # Check if DATABASE_FILE exists
        logger.info(f"The {filename} does not exist. Initializing...")
        
        sql_connection = initialize_db(filename)

        logger.info(f"Successfully initialized {filename}.")
        import_drivers(sql_connection)
        import_constructors(sql_connection)
        import_rounds(sql_connection)
        return sql_connection
    else:
        logger.info(f"{filename} already exists. Continuing with regular operations...")
        return sqlite3.connect(filename)
        

def create_new_driver(name:str, trigramme:str,car_number:int,nationality:str,sql_connection:sqlite3.Connection) -> Driver:
    '''Creates a new driver class and writes it in the Database and in the CSV file and returns the driver in the Driver class'''
    logger.info(f'Creating driver with name: {name}, trigramme: {trigramme}, car_number: {car_number}, and nationality: {nationality}')
    driver: Driver = Driver(name,trigramme,car_number,nationality)
    driver.add_to_csv()
    driver.add_to_db(sql_connection)
    return driver

def import_drivers(sql_connection:sqlite3.Connection) -> None:
    '''Imports drivers from a SCV file ("DRIVERS_FILE" in the constants.py file), with the columns "name", "trigramme","car_number", "nationality", creates the driver in the class Driver and stores it to the DB'''
    try:
        with open(DRIVERS_FILE,"r") as drivers_file:
            drivers_list = csv.reader(drivers_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
            for row_index, driver_item in enumerate(drivers_list):
                if row_index == 0:
                    continue
                driver_name: str = driver_item[DRIVERS_COLUMNS.index("name")]
                driver_trigramme: str = driver_item[DRIVERS_COLUMNS.index("trigramme")]
                driver_car_number: int = int(driver_item[DRIVERS_COLUMNS.index("car_number")])
                driver_nationality: str = driver_item[DRIVERS_COLUMNS.index("nationality")]
                logger.info(f'Importing driver with name: {driver_name}, trigramme: {driver_trigramme}, car_number: {driver_car_number}, and nationality: {driver_nationality}')
                driver: Driver = Driver(driver_name,driver_trigramme,driver_car_number,driver_nationality)
                driver.add_to_db(sql_connection)
    except FileNotFoundError:
        logger.critical(f"File {DRIVERS_FILE} not found")
        exit()

def import_constructors(sql_connection:sqlite3.Connection) -> None:
    '''Imports Constructors from a SCV file ("CONSTRUCTORS_FILE" in the constants.py file), with the columns "short_name", "full_name","result_name", "paddock_number", creates the constructors in the class Constructor and stores it to the DB'''
    try:
        with open(CONSTRUCTORS_FILE,"r") as constructor_file:
            constructor_list = csv.reader(constructor_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
            for row_index, constructor_item in enumerate(constructor_list):
                if row_index == 0:
                    continue
                constructor_short_name: str = constructor_item[CONSTRUCTORS_COLUMNS.index("short_name")]
                constructor_full_name: str = constructor_item[CONSTRUCTORS_COLUMNS.index("full_name")]
                constructor_result_name: str = constructor_item[CONSTRUCTORS_COLUMNS.index("result_name")]
                constructor_paddock_number: int = int(constructor_item[CONSTRUCTORS_COLUMNS.index("paddock_number")])
                logger.info(f'Importing constructor : {constructor_short_name}, paddock_number: {constructor_paddock_number}')
                constructor: Constructor = Constructor(constructor_full_name,constructor_result_name,constructor_short_name,constructor_paddock_number)
                constructor.add_to_db(sql_connection)
    except FileNotFoundError:
        logger.critical(f"File {CONSTRUCTORS_FILE} not found")
        exit()

def import_rounds(sql_connection:sqlite3.Connection) -> None:
    '''Imports Rounds from a SCV file ("ROUNDS_FILE" in the constants.py file), with the columns "round_number", "round_name","country", "circuit","round_date", "round_type", creates the constructors in the class Constructor and stores it to the DB'''
    try:
        with open(ROUNDS_FILE,"r") as rounds_file:
            rounds_list = csv.reader(rounds_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
            for row_index, round_item in enumerate(rounds_list):
                if row_index == 0:
                    continue
                round_number: int = int(round_item[ROUNDS_COLUMNS.index("round_number")])
                round_name: str = round_item[ROUNDS_COLUMNS.index("round_name")]
                country: str = round_item[ROUNDS_COLUMNS.index("country")]
                circuit: str = round_item[ROUNDS_COLUMNS.index("circuit")]
                round_date: str = round_item[ROUNDS_COLUMNS.index("round_date")]
                round_type: str = round_item[ROUNDS_COLUMNS.index("round_type")]
                logger.info(f'Importing Round No. : {round_number} - {round_name}')
                round: Round = Round(round_name,round_number,country,circuit,round_date,round_type)
                round.add_to_db(sql_connection)
    except FileNotFoundError:
        logger.critical(f"File {ROUNDS_FILE} not found")
        exit()

def add_results(filename:str,round_number:int, session_type:str ,sql_connection:sqlite3.Connection) -> None:
    '''For each of the results in a result_file, stored in the path RESULTS_FOLDER (specified in the constants.py file), reads the file, extract the result for each car, calculates the time for each position based on the deltas, adds the constructors paddock_number and the calculated points, and stores them in the Results Database'''
    result_file: str = RESULTS_FOLDER + filename
    try:
        with open(result_file,"r") as results:
            top_result: float = 0
            results_list = csv.reader(results, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
            for row_index, result_item in enumerate(results_list):
                if row_index == 0:
                    continue
                car_position:str = result_item[RESULTS_COLUMNS.index('Pos')]
                car_number:int = int(result_item[RESULTS_COLUMNS.index('No')])
                constructor_result_name:str = result_item[RESULTS_COLUMNS.index('Car')]
                result_time_str:str = result_item[RESULTS_COLUMNS.index('Time')]
                car_points: int = int(result_item[RESULTS_COLUMNS.index('Points')])
                try:
                    result_time_float: float = convert_time_to_seconds(result_time_str)
                    result_time_final: str 
                    if session_type in ['Race','Sprint']:
                        if row_index == 1:
                            top_result = result_time_float
                            result_time_final = str(result_time_float)
                        else:
                            result_time_float = top_result + result_time_float
                            result_time_final = str(result_time_float)
                    else:
                        result_time_final = str(result_time_float)
                except ValueError as e:
                    logger.info(f'Driver {car_number} did not finish: {result_time_str}')
                    result_time_final = result_time_str
                constructor: Constructor = get_constructor_by_resultname_fromDB(sql_connection,constructor_result_name)
                logger.info(f'Driver No. {car_number} finishing in position {car_position} has been attributed {car_points} points for session {session_type} of round {round_number}')
                result: Result = Result(car_position,car_number,constructor.paddock_number,round_number,session_type,result_time_final,car_points)
                result.add_to_db(sql_connection)
    except FileNotFoundError:
        logger.critical(f"File {filename} not found")
        exit()

def mark_round_done(sql_connection:sqlite3.Connection,round_number:int) -> None:
    '''Adds the flag round_done to the round in the Rounds Database'''
    mark_round_done_toDB(sql_connection,round_number)

def calculate_drivers_rankings(sql_connection:sqlite3.Connection,round_number:int) -> None:
    '''Calculates the driver's ranking according to the points of the sessions (and the accumulated points in the previous session) for all the cars stored in the Drivers Table, then orders the rankings and adds the position, and finally calculates if the driver has mathematical chances to win the championship. After all calculations are stored, the ranking is stored in the Drivers Ranking Table of the DB for that round.'''
    cars: list[int] = get_all_drivers_carnumber_fromDB(sql_connection)
    
    # Calculate points for each Driver for previous and current round
    drivers_points: Dict[int,int] = {}
    for car_number in cars:
        points:int = get_previous_points_driver(sql_connection,car_number,round_number) + get_points_by_driver_round_fromDB(sql_connection,car_number,round_number)
        logger.info(f'Car number {car_number} has {points} points after round No. {round_number}')
        drivers_points[car_number] = points
    
    # Generate standings list with driver positions based on points
    standings: list = [] 
    for position, (car_number, points) in enumerate(sorted(drivers_points.items(), key=lambda x: x[1], reverse=True), start=1):
        standings.append({
            'car_position': position,
            'car_number': car_number,
            'points': points
        })

    # Insert rankings into DriversRanking table    
    for ranking in standings:
        championship_chance:bool = True
        if ranking["car_position"] == 1:
            championship_chance = True
        else:
            championship_chance = is_driver_championship_chance(sql_connection,ranking["points"],round_number)
        logger.info(f'Adding Ranking for car: {ranking["car_number"]} in position {ranking["car_position"]} with {ranking["points"]} after round No. {round_number}. Championship chances: {championship_chance}.')
        driver_ranking:DriverRanking = DriverRanking(round_number,ranking["car_number"],ranking["car_position"],ranking["points"],championship_chance)
        driver_ranking.add_to_db(sql_connection)

def calculate_constructors_rankings(sql_connection:sqlite3.Connection,round_number:int) -> None:
    '''Calculates the constructors's ranking according to the points of the sessions (and the accumulated points in the previous session) for all the constructors stored in the Constructors Table, then orders the rankings and adds the position, and finally calculates if the constructor has mathematical chances to win the championship. After all calculations are stored, the ranking is stored in the Constructors Ranking Table of the DB for that round.'''
    constructors: list[int] = get_all_constructors_paddocknumber_fromDB(sql_connection)

    # Calculate points for each Constructors for each and previous round
    constructors_points: Dict[int,int] = {}
    for paddock_number in constructors:
        points: int = get_previous_points_constructor(sql_connection,paddock_number,round_number) + get_points_by_constructors_round_fromDB(sql_connection,paddock_number,round_number)
        logger.info(f'Constructor No. {paddock_number} has {points} points after round No. {round_number}')
        constructors_points[paddock_number] = points
    
    # Generate standing list with constructors position based on points
    logger.info(f'Generating constructors standing')
    standings: list = []
    for position, (paddock_number,points) in enumerate(sorted(constructors_points.items(), key=lambda x: x[1], reverse=True), start=1):
        logger.info(f'Constructor no. {paddock_number} is in {position} position with {points} by round {round_number}')
        standings.append({
            'constructor_position':position,
            'paddock_number': paddock_number,
            'points':points
        })
    logger.info(f'Final standings by round {round_number}: {standings}')
        
    # Insert rankings into Constructors Table
    for ranking in standings:
        championship_chance:bool = True
        if ranking["constructor_position"] > 1:
            championship_chance = is_constructor_championship_chance(sql_connection,ranking["points"],round_number)
        logger.info(f'Adding Ranking for constructor: {ranking["paddock_number"]} in position {ranking["constructor_position"]} with {ranking["points"]} after round No. {round_number}. Championship chances: {championship_chance}.')
        constructor_ranking:ConstructorRanking = ConstructorRanking(round_number,ranking["paddock_number"],ranking["constructor_position"],ranking["points"],championship_chance)
        constructor_ranking.add_to_db(sql_connection)

def calculate_drivers_h2h_quali(sql_connection:sqlite3.Connection,driver_1_trigramme:str,driver_2_trigramme:str) -> None:
    '''Calculates a head to head comparison between two drivers (input by trigramme, eg: VER, NOR), and returns the number of times driver 1 qualified ahead of driver 2 (and viceversa), and the average delta time between both.'''
    #Get Drivers
    driver1: Driver = get_driver_by_trigramme_fromDB(sql_connection,driver_1_trigramme)
    driver2: Driver = get_driver_by_trigramme_fromDB(sql_connection,driver_2_trigramme)
    #Get last run round
    last_round: int = get_last_round_fromDB(sql_connection)
    #Get results for Quali up to last round
    results_driver1: list[Result] = get_quali_results_by_driver_fromDB(sql_connection,driver1.car_number)
    results_driver2: list[Result] = get_quali_results_by_driver_fromDB(sql_connection,driver2.car_number)
    #Compare results
    ahead_count: dict[str,int] = {session_type: 0 for session_type in ['Q1', 'Q2', 'Q3']}
    time_diff: dict[str,list] = {session_type: [] for session_type in ['Q1', 'Q2', 'Q3']}
    for d1, d2 in zip(results_driver1,results_driver2):
        if not (hasattr(d1, 'session_type') and d1.session_type == d2.session_type and hasattr(d2, 'session_type') and d2.session_type == d1.session_type):
            continue
        if not d1.result_time.isdigit() or not d2.result_time.isdigit():
            continue
        d1_result_time = int(d1.result_time)
        d2_result_time = int(d2.result_time)

        if d1.car_position < d2.car_position:
            ahead_count[d1.session_type] += 1
        time_diff[d1.session_type].append(d2_result_time - d1_result_time)
        avg_time_diff:dict[str, int | None] = {session_type: statistics.mean(time_diffs) if time_diffs else None
                     for session_type, time_diffs in time_diff.items()}            

    #Print h2h
    for key, value in ahead_count.items():
        print(f'{key}:{value}')
    print(avg_time_diff)

    #print(f'{ahead_count=} and {avg_time_diff=}')
    #print('#### Qualification Head to Head ####')
    #print(f'Driver {driver1.name} vs Driver {driver2.name}')
    #print(f'Q3: {ahead_count["Q3"]} with {avg_time_diff["Q3"]}s')
    #print(f'Q2: {ahead_count["Q2"]} with {avg_time_diff["Q2"]}s')
    #print(f'Q1: {ahead_count["Q1"]} with {avg_time_diff["Q1"]}s')
    pass

