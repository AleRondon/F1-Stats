import sqlite3
import logging
import os
import csv
from Driver import Driver
from Constructor import Constructor
from Round import Round

logger = logging.getLogger(__name__)
LOG_FILE = ".\logs\stats.log"
LOG_FORMAT = '%(asctime)s - %(message)s'
DRIVERS_FILE = '.\database\Drivers.csv'
DRIVERS_COLUMNS = ['name','trigramme','car_number','nationality']
CONSTRUCTORS_FILE = '.\database\Constructors.csv'
CONSTRUCTORS_COLUMNS = ['full_name','short_name','paddock_number']
ROUNDS_FILE = '.\database\Rounds.csv'
ROUNDS_COLUMNS = ['round_number','round_name','country','circuit','round_date','round_type']
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

def check_and_initialize_db(filename:str) -> sqlite3.Connection:
    """Check if DATABASE_FILE exists, and call initialize_db() if it doesn't."""

    if not os.path.isfile(filename):  # Check if DATABASE_FILE exists
        logger.info(f"The {filename} does not exist. Initializing...")
        
        sql_connection = initialize_db(filename)

        logger.info(f"Successfully initialized {filename}.")
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
    sql_connection = sqlite3.connect(filename)
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
            round_number INTEGER UNIQUE
        )                    
    ''')
    logger.info(f"Tables Drivers, Rounds, and Constructors created in DB.")
    return sql_connection

def add_driver_to_db(driver: Driver,sql_connection) -> None:
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT OR IGNORE INTO Drivers (name, trigramme, car_number, nationality) VALUES (?,?,?,?)''',(driver.name,driver.trigramme,driver.car_number,driver.nationality,))
    sql_connection.commit()
    logger.info(f'Driver No. {driver.car_number} - {driver.name} was succesfully added to DB.')

def create_new_driver(name:str, trigramme:str,car_number:int,nationality:str,sql_connection) -> Driver:
    logger.info(f'Creating driver with name: {name}, trigramme: {trigramme}, car_number: {car_number}, and nationality: {nationality}')
    driver: Driver = Driver(name,trigramme,car_number,nationality)
    with open(DRIVERS_FILE,"a",newline="") as csvfile:
        driverDictionary: dict = {
            'name':driver.name,
            'trigramme':driver.trigramme,
            'car_number':driver.car_number,
            'nationality':driver.nationality
        }
        writer = csv.DictWriter(csvfile,fieldnames=DRIVERS_COLUMNS)
        writer.writerow(driverDictionary)
    logger.info(f'Driver No. {car_number} - {name} was succesfully created and added to CSV File.')
    add_driver_to_db(driver,sql_connection)
    return driver

def import_drivers(sql_connection) -> None:
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
            add_driver_to_db(driver,sql_connection)

def add_constructor_to_db(constructor:Constructor, sql_connection) -> None:
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT OR IGNORE INTO Constructor (full_name, short_name, paddock_number) VALUES (?,?,?)''',(constructor.full_name,constructor.short_name,constructor.paddock_number,))
    sql_connection.commit()
    logger.info(f'Constructor No. {constructor.paddock_number} - {constructor.full_name} was succesfully added to DB.')

def import_constructors(sql_connection) -> None:
    with open(CONSTRUCTORS_FILE,"r") as constructor_file:
        constructor_list = csv.reader(constructor_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, skipinitialspace=True)
        for row_index, constructor_item in enumerate(constructor_list):
            if row_index == 0:
                continue
            constructor_short_name: str = constructor_item[CONSTRUCTORS_COLUMNS.index("short_name")]
            constructor_full_name: str = constructor_item[CONSTRUCTORS_COLUMNS.index("full_name")]
            constructor_paddock_number: int = int(constructor_item[CONSTRUCTORS_COLUMNS.index("paddock_number")])
            logger.info(f'Importing constructor : {constructor_short_name}, paddock_number: {constructor_paddock_number}')
            constructor: Constructor = Constructor(constructor_full_name,constructor_short_name,constructor_paddock_number)
            add_constructor_to_db(constructor,sql_connection)

def add_round_to_db(round:Round,sql_connection) -> None:
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT OR IGNORE INTO Rounds (round_number,round_name,country,circuit,round_date,round_type) VALUES (?,?,?,?,?,?)''',(round.round_number,round.round_name,round.country,round.circuit,round.round_date,round.round_type,))
    sql_connection.commit()
    logger.info(f'Round No. {round.round_number} - {round.round_name} was succesfully added to DB.')

def import_rounds(sql_connection) -> None:
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
            add_round_to_db(round,sql_connection)

def add_results():
    pass

def calculate_standings():
    pass


