import logging
from ressources.main_functions import check_and_initialize_db, create_new_driver, add_results, mark_round_done, calculate_drivers_rankings, calculate_constructors_rankings
from ressources.data_entry import get_driver_trigramme, get_driver_car_number, get_round_number, get_session_type
from ressources.constants import LOG_FILE, LOG_FORMAT, DATABASE_FILE


logger = logging.getLogger(__name__)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

def main():
    sql_connection = check_and_initialize_db(DATABASE_FILE)
    logger.info("Program ready to run")
    while True:
        print(f"\n### Welcome to F1 Stats ##")
        print(f"1. Add a Driver")
        print(f"2. Add result for a session via CSV")
        print(f"0. Exit")
        choice = int(input('Enter your choice (1 - 0):'))
        if choice == 1:
            logger.info("Option chosen: new driver")
            driver_name: str = input("Driver name: ")
            driver_trigramme: str = get_driver_trigramme()
            driver_car_number: int = get_driver_car_number()
            driver_nationality: str = input("Driver nationality: ")
            driver = create_new_driver(driver_name,driver_trigramme,driver_car_number,driver_nationality,sql_connection)
            print(f"=== Succesfully created driver {driver.name} with car number {driver.car_number} ===")
        elif choice == 2:
            logger.info("Option chosen: add session result")
            round_number: int = get_round_number()
            session_type: str = get_session_type()
            filename: str = input("Filename: ")
            add_results(filename,round_number,session_type,sql_connection)
            if session_type == 'Race':
                mark_round_done(sql_connection,round_number)
                calculate_drivers_rankings(sql_connection,round_number)
                calculate_constructors_rankings(sql_connection,round_number)
            print("=== Succesfully imported session result ===")
        elif choice == 0:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter options 1 - 0")

if __name__ == "__main__":
    main()