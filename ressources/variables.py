from typing import Dict

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
RACE_POINTS: Dict[str, int] = {'1': 25,'2': 18,'3': 15,'4': 12,'5': 10,'6': 8,'7': 6,'8': 4,'9': 2,'10': 1,'11': 0,'12': 0,'13': 0,'14': 0,'15': 0,'16': 0,'17': 0,'18': 0,'19': 0,'20': 0,'NC': 0}
SPRINT_POINTS: Dict[str, int] = {'1': 8,'2': 7,'3': 6,'4': 5,'5': 4,'6': 3,'7': 2,'8': 1,'9': 0,'10': 0,'11': 0,'12': 0,'13': 0,'14': 0,'15': 0,'16': 0,'17': 0,'18': 0,'19': 0,'20': 0,'NC': 0}
