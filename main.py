import logging
from data.data_management import check_and_initialize_db, create_new_driver, import_drivers, import_constructors, import_rounds, add_results
from data.data_entry import get_driver_trigramme, get_driver_car_number, get_round_number, get_session_type
from variables import LOG_FILE, LOG_FORMAT, DATABASE_FILE


logger = logging.getLogger(__name__)

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

def main():
    sql_connection = check_and_initialize_db(DATABASE_FILE)
    logger.info("Program ready to run")
    while True:
        print(f"\n### Welcome to F1 Stats ##")
        print(f"1. Add a Driver")
        print(f"2. Import Drivers from CSV")
        print(f"3. Import Constructors from CSV")
        print(f"4. Import Rounds from CSV")
        print(f"5. Add result for a session via CSV")
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
            logger.info("Option chosen: import drivers")
            import_drivers(sql_connection)
            print("=== Succesfully imported drivers ===")
        elif choice == 3:
            logger.info("Option chosen: import constructors")
            import_constructors(sql_connection)
            print("=== Succesfully imported constructors ===")
        elif choice == 4:
            logger.info("Option chosen: import rounds")
            import_rounds(sql_connection)
            print("=== Succesfully imported rounds ===")
        elif choice == 5:
            logger.info("Option chosen: add session result")
            round_number: int = get_round_number()
            session_type: str = get_session_type()
            filename: str = input("Filename: ")
            add_results(filename,round_number,session_type,sql_connection)
            print("=== Succesfully imported session result ===")
        elif choice == 0:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter options 1 - 0")

if __name__ == "__main__":
    main()