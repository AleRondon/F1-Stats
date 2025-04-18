from typing import Dict,Union

DATABASE_FILE: str = '.\\data\\database\\stats-database.sqlite'
LOG_FILE: str = '.\\stats.log'
LOG_FORMAT: str = '%(asctime)s - %(message)s'
ROUNDS_FILE: str = '.\\data\\Rounds.csv'
DRIVERS_FILE: str = '.\\data\\Drivers.csv'
CONSTRUCTORS_FILE: str = '.\\data\\Constructors.csv'
DRIVERS_COLUMNS: list[str] = ['name','trigramme','car_number','nationality']
CONSTRUCTORS_COLUMNS: list[str] = ['full_name','result_name','short_name','paddock_number']
ROUNDS_COLUMNS: list[str] = ['round_number','round_name','country','circuit','round_date','round_type']
RESULTS_FOLDER: str = ".\\data\\results\\"
RESULTS_COLUMNS: list[str] = ['Pos','No','Driver','Car','Time']
VALID_SESSION_TYPES: list[str] = ['Race','Q1','Q2','Q3','Sprint','SQ1','SQ2','SQ3']
RACE_POINTS: Dict[Union[int, str], int] = {
    1: 25,
    2: 18,
    3: 15,
    4: 12,
    5: 10,
    6: 8,
    7: 6,
    8: 4,
    9: 2,
    10: 1,
    'NC': 0, # For non-completers
    **{i: 0 for i in range(11, 21)} # Adding keys from 11 to 20 with values set to 0.
}
SPRINT_POINTS: Dict[Union[int, str], int] = {
    1: 8,
    2: 7,
    3: 6,
    4: 5,
    5: 4,
    6: 3,
    7: 2,
    8: 1,
    'NC': 0, # For non-completers
    **{i: 0 for i in range(9, 21)} # Adding keys from 9 to 20 with values set to 0.
}
