import logging
from ressources.constants import LOG_FILE, LOG_FORMAT

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class ConstructorRanking:
    def __init__(self,round_number:int,paddock_number:int,constructor_position:int,constructor_points:int,championship_chance:bool):
        self.round_number: int = round_number
        self.paddock_number: int = paddock_number
        self.constructor_position: int = constructor_position
        self.constructor_points: int = constructor_points
        self.championship_chance: bool = championship_chance

    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        try:
            sql_cursor.execute('''INSERT OR IGNORE INTO ConstructorsRanking (round_number,paddock_number,constructor_position,constructor_points,championship_chance) VALUES (?,?,?,?,?)''',(self.round_number,self.paddock_number,self.constructor_position,self.constructor_points,self.championship_chance,))
            sql_connection.commit()
            logger.info(f'Ranking added to DB for constructor: {self.paddock_number} in position {self.constructor_position} with {self.constructor_points} after round No. {self.round_number}. Championship chances: {self.championship_chance}.')
        except Exception as e:
            logger.error(f'Error {e} detected when trying to commit ranking for constructor No. {self.paddock_number} in round No. {self.round_number}')


    
