import logging

logger = logging.getLogger(__name__)
LOG_FILE = ".\logs\stats.log"
LOG_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class Result:
    def __init__(self,car_position:int,car_number:int,team:int,round_number: int,round_type: str,time: str):
       self.car_position: int = car_position
       self.car_number: int = car_number
       self.team: int = team
       self.round_number: int = round_number
       self.round_type: str = round_type
       self.time: str = time
    
    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        sql_cursor.execute('''INSERT OR IGNORE INTO Constructor (car_position, car_number, team,round_number, round_type,time) VALUES (?,?,?,?,?,?)''',(self.car_position,self.car_number,self.team,self.round_number,self.round_type,self.time))
        sql_connection.commit()
        logger.info(f'Result of Car No. {self.car_number} for Round No.- {self.round_number} was succesfully added to DB.')

