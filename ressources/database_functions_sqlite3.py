import sqlite3
import logging
from ressources.classes.Constructor import Constructor
from ressources.classes.ConstructorRanking import ConstructorRanking
from ressources.classes.Driver import Driver
from ressources.classes.DriverRanking import DriverRanking
from ressources.classes.Result import Result
from ressources.classes.Round import Round
from ressources.constants import LOG_FILE,LOG_FORMAT,TOTAL_RACES,TOTAL_SPRINTS

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

#############################################################################
####                    Initalize DB                                     ####
#############################################################################

def initialize_db(filename:str) -> sqlite3.Connection:
    '''Initialises the database with the required tables of Drivers, Constructors, Rounds, Results, DriversRanking and ConstructorsRanking'''
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

        CREATE TABLE Constructors (
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
            paddock_number INT,
            session_type TEXT,
            result_time TEXT,
            car_points INT,                            
            PRIMARY KEY (round_number,car_number,session_type)
        );
        CREATE TABLE ConstructorsRanking (
            round_number INT,
            paddock_number INT,
            constructor_position INT,
            constructor_points INT,
            championship_chance BOOLEAN,
            PRIMARY KEY (round_number, paddock_number)
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

#############################################################################
####                         Drivers                                     ####
#############################################################################

def add_driver_toDB(sql_connection:sqlite3.Connection,driver: Driver) -> None:
    '''Adds a new driver into the Drivers Table of the Database'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT OR IGNORE INTO Drivers (name, trigramme, car_number, nationality) VALUES (?,?,?,?)''',(driver.name,driver.trigramme,driver.car_number,driver.nationality,))
    sql_connection.commit()
    logger.info(f'Driver No. {driver.car_number} - {driver.name} was succesfully added to DB.')

def get_driver_by_trigramme_fromDB(sql_connection:sqlite3.Connection,trigramme: str) -> Driver:
    '''Fetches Driver from the Drivers Table based on the trigramme of the Driver (eg. VER, NOR)'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''Select name, car_number, nationality from Drivers where trigramme = ?''',(trigramme,))
    result = sql_cursor.fetchone()
    name:str = result[0]
    car_number:int = result[1]
    nationality:str = result[2]
    driver:Driver = Driver(name,trigramme,car_number,nationality)
    logger.info(f'Class instanciated for driver {trigramme}')
    return driver

def get_driver_by_carnumber_fromDB(sql_connection:sqlite3.Connection,car_number: int) -> Driver:
    '''Fetches Driver from the Drivers Table based on the car number (eg. 1, 16)'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''Select name, trigramme, nationality from Drivers where car_number = ?''',(car_number,))
    result = sql_cursor.fetchone()
    name:str = result[0]
    trigramme:str = result[1]
    nationality:str = result[2]
    driver:Driver = Driver(name,trigramme,car_number,nationality)
    logger.info(f'Class instanciated for driver No. {car_number}')
    return driver

def get_all_drivers_carnumber_fromDB(sql_connection:sqlite3.Connection) -> list[int]:
    '''Fetches a list of car numbers for all the drivers in Drivers Table'''
    logger.info('Fetching list of drivers in Drivers Table')
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('SELECT car_number FROM Drivers')
    car_numbers: list[int] = [int(car[0]) for car in sql_cursor.fetchall()]
    logger.info(f'{len(car_numbers)} car numbers retrieved from Drivers Table')
    return car_numbers

#############################################################################
####                       Constructors                                  ####
#############################################################################

def add_constructor_toDB(sql_connection:sqlite3.Connection,constructor: Constructor) -> None:
    '''Adds a new constructor into the Constructors Table of the Database'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT OR IGNORE INTO Constructors (full_name,result_name, short_name, paddock_number) VALUES (?,?,?,?)''',(constructor.full_name,constructor.result_name,constructor.short_name,constructor.paddock_number,))
    sql_connection.commit()
    logger.info(f'Constructor No. {constructor.paddock_number} - {constructor.full_name} was succesfully added to DB.')

def get_constructor_by_resultname_fromDB(sql_connection:sqlite3.Connection,result_name:str) -> Constructor:
    '''Fetches Constructor from the Constructors Table based on the result name -Car & Engine Manufacturer- (eg. McLaren Mercedes, Haas Ferrari)'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('SELECT full_name, short_name,paddock_number FROM Constructors WHERE result_name = ? ', (result_name, ))
    result = sql_cursor.fetchone()
    full_name: str = result[0]
    short_name: str = result[1]
    paddock_number: int = result[2]
    constructor:Constructor = Constructor(full_name,result_name,short_name,paddock_number)
    logger.info(f'Class instanciated for constructor {result_name}')
    return constructor

def get_all_constructors_paddocknumber_fromDB(sql_connection:sqlite3.Connection) -> list[int]:
    '''Fetches a list of paddock numbers for all the constructors in Copnstructor Table'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('Select paddock_number FROM Constructors')
    paddock_numbers: list[int] = [int(constructor[0]) for constructor in sql_cursor.fetchall()]
    logger.info(f'{len(paddock_numbers)} paddock numbers retrieved from Constructors Table')
    return paddock_numbers
   

#############################################################################
####                          Rounds                                     ####
#############################################################################

def add_round_toDB(sql_connection:sqlite3.Connection,round:Round) -> None:
    '''Adds a new round into the Rounds Table of the Database'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT INTO Rounds (round_number,round_name,country,circuit,round_date,round_type,round_finished) VALUES (?,?,?,?,?,?,?)''',(round.round_number,round.round_name,round.country,round.circuit,round.round_date,round.round_type,round.round_finished,))
    sql_connection.commit()
    logger.info(f'Round No. {round.round_number} - {round.round_name} was succesfully added to DB.')

def mark_round_done_toDB(sql_connection:sqlite3.Connection,round_number:int) -> None:
    '''Updates round in Rounds Table to mark round_done as true'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''UPDATE Rounds SET round_finished = true WHERE round_number = ?''',(round_number,))
    sql_connection.commit()
    logger.info(f'Round No. {round_number} - Marked as done in DB.')

def get_done_races_fromDB(sql_connection:sqlite3.Connection) -> int:
    '''Fetches number of races completed in the Rounds Table of the Database'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''SELECT COUNT(round_number) FROM ROUNDS WHERE round_finished = 1''')
    result = sql_cursor.fetchone()
    done_races: int = result[0]
    logger.info(f'{done_races} races has been finished out of {TOTAL_RACES}')
    return done_races

def get_done_sprints_fromDB(sql_connection:sqlite3.Connection) -> int:
    '''Fetches number of sprints completed in the Rounds Table of the Database'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''SELECT COUNT(round_number) FROM ROUNDS WHERE round_type = "Sprint" AND round_finished = 1''')
    result = sql_cursor.fetchone()
    done_sprints: int = result[0]
    logger.info(f'{done_sprints} sprints has been finished out of {TOTAL_SPRINTS}')
    return done_sprints

def get_last_round_fromDB(sql_connection:sqlite3.Connection) -> int:
    '''Fetches the number of the last round marked as done in the Rounds Table of the Database'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''SELECT round_number FROM Rounds WHERE round_finished = 1 ORDER BY round_number DESC''')
    round_number:int = sql_cursor.fetchone()[0]
    logger.info(f'Last round ran is No. {round_number}')
    return round_number

#############################################################################
####                          Results                                    ####
#############################################################################

def add_results_toDB(sql_connection:sqlite3.Connection,result:Result) -> None:
    '''Adds a new result into the Results Table of the Database'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT INTO Results (car_position, car_number, paddock_number,round_number, session_type,result_time,car_points) VALUES (?,?,?,?,?,?,?)''',(result.car_position,result.car_number,result.paddock_number,result.round_number,result.session_type,result.result_time,result.car_points))
    sql_connection.commit()
    logger.info(f'Result for session {result.session_type} of Car No. {result.car_number} for Round No.- {result.round_number} was succesfully added to DB.')

def get_points_by_driver_round_fromDB(sql_connection:sqlite3.Connection,car_number:int,round_number:int) -> int:
    '''Fetches the sum of points (Race and Sprint) of a Driver (by car number) and Round (by round number) from the Results Table of the Database'''
    sql_cursor = sql_connection.cursor()
    logger.info(f'Fetching points for Driver No. {car_number} by round No. {round_number}')
    sql_cursor.execute('''SELECT SUM(car_points) FROM Results WHERE round_number = ? and car_number = ?''',(round_number,car_number,))
    points:int = sql_cursor.fetchone()[0]
    logger.info(f'Driver No. {car_number} has {points} points by round No. {round_number}')
    return points

def get_quali_results_by_driver_fromDB(sql_connection:sqlite3.Connection,car_number:int) -> list[Result]:
    '''Fetches all the results for qualification sessions of a driver based on the car number'''
    sql_cursor = sql_connection.cursor()
    results_list: list = list()
    sql_cursor.execute('''SELECT car_position,paddock_number,round_number,session_type,result_time,car_points FROM Results WHERE car_number = ? AND (session_type = "Q1" OR session_type = "Q2" OR session_type = "Q3") ORDER BY round_number''',(car_number,))
    sql_results: list = sql_cursor.fetchall()
    for sql_result in sql_results:
        car_position: str = sql_result[0]
        paddock_number: int = sql_result[1]
        round_number: int = sql_result[2]
        session_type: str = sql_result[3]
        result_time: str = sql_result[4]
        car_points: int = sql_result[5]
        result: Result = Result(car_position,car_number,paddock_number,round_number,session_type,result_time,car_points)
        results_list.append(result)
    logger.info(f'Driver No. {car_number} has {len(results_list)} results for Qualification Sessions')
    return results_list

def get_sprint_quali_results_by_driver_fromDB(sql_connection:sqlite3.Connection,car_number:int) -> list[Result]:
    '''Fetches all the results for qualification sessions of a driver based on the car number'''
    sql_cursor = sql_connection.cursor()
    results_list: list = list()
    sql_cursor.execute('''SELECT car_position,paddock_number,round_number,session_type,result_time,car_points FROM Results WHERE car_number = ? AND (session_type = "SQ1" OR session_type = "SQ2" OR session_type = "SQ3") ORDER BY round_number''',(car_number,))
    sql_results: list = sql_cursor.fetchall()
    for sql_result in sql_results:
        car_position: str = sql_result[0]
        paddock_number: int = sql_result[1]
        round_number: int = sql_result[2]
        session_type: str = sql_result[3]
        result_time: str = sql_result[4]
        car_points: int = sql_result[5]
        result: Result = Result(car_position,car_number,paddock_number,round_number,session_type,result_time,car_points)
        results_list.append(result)
    logger.info(f'Driver No. {car_number} has {len(results_list)} results for Qualification Sessions')
    return results_list

def get_race_results_by_driver_fromDB(sql_connection:sqlite3.Connection,car_number:int) -> list[Result]:
    '''Fetches all the results for qualification sessions of a driver based on the car number'''
    sql_cursor = sql_connection.cursor()
    results_list: list = list()
    sql_cursor.execute('''SELECT car_position,paddock_number,round_number,session_type,result_time,car_points FROM Results WHERE car_number = ? AND (session_type = "Race") ORDER BY round_number''',(car_number,))
    sql_results: list = sql_cursor.fetchall()
    for sql_result in sql_results:
        car_position: str = sql_result[0]
        paddock_number: int = sql_result[1]
        round_number: int = sql_result[2]
        session_type: str = sql_result[3]
        result_time: str = sql_result[4]
        car_points: int = sql_result[5]
        result: Result = Result(car_position,car_number,paddock_number,round_number,session_type,result_time,car_points)
        results_list.append(result)
    logger.info(f'Driver No. {car_number} has {len(results_list)} results for Qualification Sessions')
    return results_list

def get_sprint_results_by_driver_fromDB(sql_connection:sqlite3.Connection,car_number:int) -> list[Result]:
    '''Fetches all the results for qualification sessions of a driver based on the car number'''
    sql_cursor = sql_connection.cursor()
    results_list: list = list()
    sql_cursor.execute('''SELECT car_position,paddock_number,round_number,session_type,result_time,car_points FROM Results WHERE car_number = ? AND (session_type = "Sprint") ORDER BY round_number''',(car_number,))
    sql_results: list = sql_cursor.fetchall()
    for sql_result in sql_results:
        car_position: str = sql_result[0]
        paddock_number: int = sql_result[1]
        round_number: int = sql_result[2]
        session_type: str = sql_result[3]
        result_time: str = sql_result[4]
        car_points: int = sql_result[5]
        result: Result = Result(car_position,car_number,paddock_number,round_number,session_type,result_time,car_points)
        results_list.append(result)
    logger.info(f'Driver No. {car_number} has {len(results_list)} results for Qualification Sessions')
    return results_list

def get_points_by_constructors_round_fromDB(sql_connection:sqlite3.Connection,paddock_number:int,round_number:int) -> int:
    '''Fetches the sum of points (Race and Sprint) of a Constructors (by paddoc number, both drivers) and Round (by round number) from the Results Table of the Database'''
    logger.info(f'Fetching points for Constructor No. {paddock_number} by round No. {round_number}')
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''SELECT SUM(car_points) FROM Results WHERE round_number = ? and paddock_number = ?''',(round_number,paddock_number,))
    points:int = sql_cursor.fetchone()[0]
    logger.info(f'Constructor No. {paddock_number} has {points} points by round No. {round_number}')
    return points

    

#############################################################################
####                       Driver's Rankings                             ####
#############################################################################

def add_drivers_ranking_toDB(sql_connection:sqlite3.Connection,driver_ranking:DriverRanking) -> None:
    '''Adds a new driver's ranking into the Drivers Ranking Table of the Database'''
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT INTO DriversRanking (round_number,car_number,car_position,car_points,championship_chance) VALUES (?,?,?,?,?)''',(driver_ranking.round_number,driver_ranking.car_number,driver_ranking.car_position,driver_ranking.car_points,driver_ranking.championship_chance,))
    sql_connection.commit()
    logger.info(f'Ranking added to DB for car: {driver_ranking.car_number} in position {driver_ranking.car_position} with {driver_ranking.car_points} after round No. {driver_ranking.round_number}. Championship chances: {driver_ranking.championship_chance}.')

def get_points_by_driver_ranking_fromDB(sql_connection:sqlite3.Connection,round_number:int,car_number:int) -> int:
    '''Fetches a drivers points from the ranking for an specific round from the Drivers Ranking Table of the Database'''
    sql_cursor = sql_connection.cursor()
    logger.info(f'Fetching points for driver No. {car_number} by round No. {round_number}')
    sql_cursor.execute('''SELECT car_points FROM DriversRanking WHERE round_number = ? and car_number = ?''',(round_number,car_number,))
    points = sql_cursor.fetchone()[0]
    logger.info(f'Retrieved {points} for driver No. {car_number} by round No. {round_number}')
    return points
    
def get_points_of_P1_Driver_fromDB(sql_connection:sqlite3.Connection,round_number:int) -> int:
    '''Fetches the points of the driver in P1 by round number from the Drivers Ranking Table of the Database'''
    sql_cursor = sql_connection.cursor()
    logger.info(f'Fetching for driver in P1 by round No. {round_number}')
    sql_cursor.execute('''SELECT car_points FROM DriversRanking WHERE round_number = ? and car_position = 1''',(round_number,))
    result = sql_cursor.fetchone()
    points = result[0]
    logger.info(f'Retrieved {points} points for driver in P1 by round No. {round_number}')
    return points
    

#############################################################################
####                       Constructors's Rankings                       ####
#############################################################################

def add_constructor_ranking_toDB(sql_connection:sqlite3.Connection,constructor_ranking:ConstructorRanking) -> None:
    '''Adds a new constructor's ranking into the Constructors Ranking Table of the Database'''
    logger.info(f'Adding ranking to DB for constructor: {constructor_ranking.paddock_number} in position {constructor_ranking.constructor_position} with {constructor_ranking.constructor_points} after round No. {constructor_ranking.round_number}. Championship chances: {constructor_ranking.championship_chance}.')
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''INSERT INTO ConstructorsRanking (round_number,paddock_number,constructor_position,constructor_points,championship_chance) VALUES (?,?,?,?,?)''',(constructor_ranking.round_number,constructor_ranking.paddock_number,constructor_ranking.constructor_position,constructor_ranking.constructor_points,constructor_ranking.championship_chance,))
    sql_connection.commit()
    logger.info(f'Ranking added to DB for constructor: {constructor_ranking.paddock_number} in position {constructor_ranking.constructor_position} with {constructor_ranking.constructor_points} after round No. {constructor_ranking.round_number}. Championship chances: {constructor_ranking.championship_chance}.')
    
def get_points_by_constructors_ranking_fromDB(sql_connection:sqlite3.Connection,round_number:int,paddock_number:int) -> int:
    '''Fetches a constructors points from the ranking for an specific round from the Constructors Ranking Table of the Database'''
    logger.info(f'Fetching points for constructor No. {paddock_number} by round No. {round_number}')
    sql_cursor = sql_connection.cursor()
    sql_cursor.execute('''SELECT constructor_points FROM ConstructorsRanking WHERE round_number = ? and paddock_number = ?''',(round_number,paddock_number,))
    points = sql_cursor.fetchone()[0]
    logger.info(f'Retrieved {points} points for constructor No. {paddock_number} by round No. {round_number}')
    return points

def get_points_of_P1_Constructor_fromDB(sql_connection:sqlite3.Connection,round_number:int) -> int:
    '''Fetches the points of the constructor in P1 by round number from the Constructors Ranking Table of the Database'''
    sql_cursor = sql_connection.cursor()
    logger.info(f'Fetching points for constructor in P1 by round No. {round_number}')
    sql_cursor.execute('''SELECT constructor_points FROM ConstructorsRanking WHERE round_number = ? and constructor_position = 1''',(round_number,))
    points = sql_cursor.fetchone()[0]
    logger.info(f'Retrieved {points} points for constructor in P1 by round No. {round_number}')
    return points