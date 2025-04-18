import logging
from ressources.variables import LOG_FILE, LOG_FORMAT

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class Result:
    def __init__(self,car_position:str,car_number:int,constructor_number:int,round_number: int,session_type: str,result_time: str,car_points:int):
       self.car_position: str = car_position
       self.car_number: int = car_number
       self.constructor_number: int = constructor_number
       self.round_number: int = round_number
       self.session_type: str = session_type
       self.result_time: str = result_time
       self.car_points: int = car_points
    
    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        sql_cursor.execute('''INSERT OR IGNORE INTO Results (car_position, car_number, constructor_number,round_number, session_type,result_time,car_points) VALUES (?,?,?,?,?,?,?)''',(self.car_position,self.car_number,self.constructor_number,self.round_number,self.session_type,self.result_time,self.car_points))
        sql_connection.commit()
        logger.info(f'Result for session {self.session_type} of Car No. {self.car_number} for Round No.- {self.round_number} was succesfully added to DB.')

