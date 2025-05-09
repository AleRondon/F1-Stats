import logging
from ressources.constants import LOG_FILE, LOG_FORMAT

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class Result:
    def __init__(self,car_position:str,car_number:int,paddock_number:int,round_number: int,session_type: str,result_time: str,car_points:int):
       self.car_position: str = car_position
       self.car_number: int = car_number
       self.paddock_number: int = paddock_number
       self.round_number: int = round_number
       self.session_type: str = session_type
       self.result_time: str = result_time
       self.car_points: int = car_points
    
    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        try:
            sql_cursor.execute('''INSERT INTO Results (car_position, car_number, paddock_number,round_number, session_type,result_time,car_points) VALUES (?,?,?,?,?,?,?)''',(self.car_position,self.car_number,self.paddock_number,self.round_number,self.session_type,self.result_time,self.car_points))
            sql_connection.commit()
            logger.info(f'Result for session {self.session_type} of Car No. {self.car_number} for Round No.- {self.round_number} was succesfully added to DB.')
        except Exception as e:
            logger.error(f'Error {e} detected when trying to commit result for car No. {self.car_number} in round No. {self.round_number} for session {self.session_type}')

