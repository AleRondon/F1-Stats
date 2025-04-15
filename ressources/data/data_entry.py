import re
import logging
from ressources.variables import LOG_FILE, LOG_FORMAT, VALID_SESSION_TYPES

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

def get_round_number() -> int:
    try:
        round_number: int = int(input("Round number:"))
        if round_number < 1 or round_number > 24:
            raise ValueError("Only rounds from 1 to 24")
        return round_number
    except ValueError as e:
        print(e)
        logger.warning("Wrong round number selected")
        return get_round_number()
    
def get_session_type() -> str:
    try:
        session_type: str = input("Session type:")
        if session_type not in VALID_SESSION_TYPES:
            raise ValueError(f'Invalid session type, please select a valid one, between this list: {VALID_SESSION_TYPES}')
        return session_type
    except ValueError as e:
        print(e)
        logger.warning("Wrong session type")
        return get_session_type()


