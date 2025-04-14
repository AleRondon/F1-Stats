import logging

logger = logging.getLogger(__name__)
LOG_FILE = ".\logs\stats.log"
LOG_FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class Constructor:
    def __init__(self,full_name: str, short_name: str, paddock_number: int):
        self.full_name: str = full_name
        self.short_name: str = short_name
        self.paddock_number: int = paddock_number

    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        sql_cursor.execute('''INSERT OR IGNORE INTO Constructor (full_name, short_name, paddock_number) VALUES (?,?,?)''',(self.full_name,self.short_name,self.paddock_number,))
        sql_connection.commit()
        logger.info(f'Constructor No. {self.paddock_number} - {self.full_name} was succesfully added to DB.')