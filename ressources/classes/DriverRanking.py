import logging
from ressources.constants import LOG_FILE, LOG_FORMAT

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class DriverRanking:
    def __init__(self,round_number:int,car_number:int,car_position:int,car_points:int,championship_chance:bool):
        self.round_number: int = round_number
        self.car_number: int = car_number
        self.car_position: int = car_position
        self.car_points: int = car_points
        self.championship_chance: bool = championship_chance

    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        sql_cursor.execute('''INSERT OR IGNORE INTO DriversRanking (round_number,car_number,car_position,car_points,championship_chance) VALUES (?,?,?,?,?)''',(self.round_number,self.car_number,self.car_position,self.car_points,self.championship_chance,))
        sql_connection.commit()
        logger.info(f'Ranking added to DB for car: {self.car_number} in position {self.car_position} with {self.car_points} after round No. {self.round_number}. Championship chances: {self.championship_chance}.')
    
