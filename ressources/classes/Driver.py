import logging
import csv
from ressources.constants import LOG_FILE, LOG_FORMAT, DRIVERS_FILE, DRIVERS_COLUMNS

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

class Driver:
    def __init__(self,name: str,trigramme: str,car_number: int,nationality: str):
        self.name: str = name
        self.trigramme: str = trigramme
        self.car_number: int = car_number
        self.nationality: str = nationality
    
    def add_to_db(self,sql_connection) -> None:
        sql_cursor = sql_connection.cursor()
        sql_cursor.execute('''INSERT OR IGNORE INTO Drivers (name, trigramme, car_number, nationality) VALUES (?,?,?,?)''',(self.name,self.trigramme,self.car_number,self.nationality,))
        sql_connection.commit()
        logger.info(f'Driver No. {self.car_number} - {self.name} was succesfully added to DB.')
        
    def add_to_csv(self) -> None:
        try:
            with open(DRIVERS_FILE,"a",newline="") as csvfile:
                driverDictionary: dict = {
                    'name':self.name,
                    'trigramme':self.trigramme,
                    'car_number':self.car_number,
                    'nationality':self.nationality
                }
                writer = csv.DictWriter(csvfile,fieldnames=DRIVERS_COLUMNS)
                writer.writerow(driverDictionary)
            logger.info(f'Driver No. {self.car_number} - {self.name} was succesfully added to CSV File.')
        except FileNotFoundError:
            logger.critical(f"File {DRIVERS_FILE} not found")
            exit()
