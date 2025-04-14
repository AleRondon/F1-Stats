import logging

logger = logging.getLogger(__name__)
LOG_FILE = ".\logs\stats.log"
LOG_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class Round:
    def __init__(self,round_name:str,round_number:int,country:str,circuit:str,round_date:str,round_type:str):
        self.round_name: str = round_name
        self.round_number: int = round_number
        self.country: str = country
        self.circuit: str = circuit
        self.round_date: str = round_date
        self.round_type: str = round_type

    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        sql_cursor.execute('''INSERT OR IGNORE INTO Rounds (round_number,round_name,country,circuit,round_date,round_type) VALUES (?,?,?,?,?,?)''',(self.round_number,self.round_name,self.country,self.circuit,self.round_date,self.round_type,))
        sql_connection.commit()
        logger.info(f'Round No. {self.round_number} - {self.round_name} was succesfully added to DB.')
    
