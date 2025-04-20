import logging
from ressources.constants import LOG_FILE, LOG_FORMAT

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class Round:
    def __init__(self,round_name:str,round_number:int,country:str,circuit:str,round_date:str,round_type:str):
        self.round_name: str = round_name
        self.round_number: int = round_number
        self.country: str = country
        self.circuit: str = circuit
        self.round_date: str = round_date
        self.round_type: str = round_type
        self.round_finished: bool = False

    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        try:
            sql_cursor.execute('''INSERT INTO Rounds (round_number,round_name,country,circuit,round_date,round_type,round_finished) VALUES (?,?,?,?,?,?,?)''',(self.round_number,self.round_name,self.country,self.circuit,self.round_date,self.round_type,self.round_finished,))
            sql_connection.commit()
            logger.info(f'Round No. {self.round_number} - {self.round_name} was succesfully added to DB.')
        except Exception as e:
            logger.error(f'Error {e} detected when trying to commit round No. {self.round_number} - {self.round_name}')
        
