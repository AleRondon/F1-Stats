import sqlite3
import logging
import os
import csv
from typing import Dict
from ressources.classes.Driver import Driver
from ressources.classes.Constructor import Constructor
from ressources.classes.Round import Round
from ressources.classes.Result import Result
from ressources.helper_functions import convert_time_to_seconds, attribute_points
from ressources.variables import LOG_FILE, LOG_FORMAT, DRIVERS_FILE, DRIVERS_COLUMNS, CONSTRUCTORS_FILE, CONSTRUCTORS_COLUMNS, ROUNDS_FILE, ROUNDS_COLUMNS, RESULTS_FOLDER, RESULTS_COLUMNS

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
        
def initialize_db(filename:str) -> sqlite3.Connection:
    ''' Initialises the database with the required tables
        
        Parameters:
        -----------        
        filename: str 
            The file name of the sqlite database file to be initialized.
        
        Returns:
        -----------
        An sqllite3 connection to be used in for updating and reading the database.
    '''
    logger.info(f"Creating and connecting to {filename}.")
    try:
        sql_connection = sqlite3.connect(filename)
    except sqlite3.OperationalError as e:
        logger.critical(f"Error accesing the DB: {e}")
        exit()
    sql_cursor = sql_connection.cursor()
    logger.info(f"Creating tables in the database.")
    sql_cursor.executescript('''
        CREATE TABLE Drivers (
            id     INTEGER PRIMARY KEY,
            name   TEXT,
            trigramme TEXT,
            car_number INTEGER UNIQUE,
            nationality TEXT                         
        );

        CREATE TABLE Constructor (
            id     INTEGER PRIMARY KEY,
            full_name  TEXT,
            result_name  TEXT,
            short_name TEXT,
            paddock_number INTEGER UNIQUE
        );
        CREATE TABLE Rounds (
            id     INTEGER PRIMARY KEY,
            round_name  TEXT,
            country TEXT,
            circuit TEXT,
            round_date TEXT,
            round_type TEXT,
            round_finished BOOLEAN,                                              
            round_number INTEGER UNIQUE
            
        );
        CREATE TABLE Results (
            round_number  INT,
            car_position TEXT,
            car_number INT,
            constructor_number INT,
            session_type TEXT,
            result_time TEXT,
            car_points INT,                            
            PRIMARY KEY (round_number,car_number,session_type)
        );
        CREATE TABLE ConstructorsRanking (
            round_number INT,
            constructor_paddock_number INT,
            constructor_position INT,
            constructor_points INT,
            championship_chance BOOLEAN,
            PRIMARY KEY (round_number, constructor_paddock_number)
        );
        CREATE TABLE DriversRanking (
            round_number INT,
            car_number INT,
            car_position INT,
            car_points INT,
            championship_chance BOOLEAN,
            PRIMARY KEY (round_number, car_number)
        )
    ''')
    logger.info(f"Tables Drivers, Rounds, and Constructors created in DB.")
    return sql_connection

def create_new_driver(name:str, trigramme:str,car_number:int,nationality:str,sql_connection) -> Driver:
    logger.info(f'Creating driver with name: {name}, trigramme: {trigramme}, car_number: {car_number}, and nationality: {nationality}')
    driver: Driver = Driver(name,trigramme,car_number,nationality)
    driver.add_to_csv()
    driver.add_to_db(sql_connection)
    return driver

def import_drivers(sql_connection) -> None:
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

def import_constructors(sql_connection) -> None:
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

def import_rounds(sql_connection) -> None:
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

def add_results(filename:str,round_number:int, session_type:str ,sql_connection) -> None:
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
                sql_cursor = sql_connection.cursor()
                sql_cursor.execute('SELECT paddock_number FROM Constructor WHERE result_name = ? ', (constructor_result_name, ))
                constructor_number = sql_cursor.fetchone()[0]
                car_points: int = attribute_points(car_position,session_type)
                logger.info(f'Driver No. {car_number} finishing in position {car_position} has been attributed {car_points} points for session {session_type} of round {round_number}')
                result: Result = Result(car_position,car_number,constructor_number,round_number,session_type,result_time_final,car_points)
                result.add_to_db(sql_connection)
    except FileNotFoundError:
        logger.critical(f"File {filename} not found")
        exit()

def mark_round_done(sql_connection,round_number:int) -> None:
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''UPDATE Rounds SET round_finished = true WHERE round_number = ?''',(round_number,))
    sql_connection.commit()

def calculate_drivers_rankings(sql_connection,round_number:int) -> None:
    # -> Get Previous Points for all drivers
    # -> Add Points for this round
    # -> Update list of Standings
    pass
    



'''
# Here's a sample data of drivers and their points.
drivers_points = {
    'Hamilton': 418,
    'Vettel': 306,
    'Ricciardo': 220,
    'Raikkonen': 178,
    'Bottas': 159
}

# Create an empty list to store the standings.
standings = []

# Iterate over each driver and their points in descending order of points.
for position, (driver, points) in enumerate(sorted(drivers_points.items(), key=lambda x: x[1], reverse=True), start=1):
    # Add a dictionary containing driver's name, points, and position to the standings list.
    standings.append({
        'position': position,
        'driver': driver,
        'points': points
    })

# Print the standings for our young apprentice Ale.
print(standings)
'''
        
   








    

