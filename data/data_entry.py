import re
import logging
from variables import LOG_FILE, LOG_FORMAT

logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

def get_driver_trigramme() -> str:
    driver_trigramme: str = input('Driver trigramme: ')
    try:
        pattern: str = "^[A-Z]{3}$"
        if not bool(re.match(pattern,driver_trigramme)):
            raise ValueError("Trigramme should be 3 uppercase letters, e.g. VER, NOR")
        return driver_trigramme
    except ValueError as e:
        print(e)
        logger.warning("Wrong trigramme selected")
        return get_driver_trigramme()

def get_driver_car_number() -> int:
    try:
        driver_car_number: int = int(input("Driver car number: "))
        if driver_car_number < 1 and driver_car_number >= 100:
            raise ValueError("Number should be a number between 1 and 100")
        return driver_car_number
    except ValueError as e:
        print(e)
        logger.warning("Wrong car number selected")
        return get_driver_car_number()