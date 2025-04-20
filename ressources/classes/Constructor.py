import logging
from ressources.constants import LOG_FILE, LOG_FORMAT

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class Constructor:
    def __init__(self,full_name: str,result_name: str, short_name: str, paddock_number: int):
        self.full_name: str = full_name
        self.result_name: str = result_name
        self.short_name: str = short_name
        self.paddock_number: int = paddock_number

    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        try:
            sql_cursor.execute('''INSERT INTO Constructors (full_name,result_name, short_name, paddock_number) VALUES (?,?,?,?)''',(self.full_name,self.result_name,self.short_name,self.paddock_number,))
            sql_connection.commit()
            logger.info(f'Constructor No. {self.paddock_number} - {self.full_name} was succesfully added to DB.')
        except Exception as e:
            logger.error(f'Error {e} detected when trying to commit Constructor No. {self.paddock_number} - {self.full_name}')