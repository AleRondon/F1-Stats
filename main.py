import logging
from ressources.main_functions import check_and_initialize_db, create_new_driver, add_results, mark_round_done, calculate_drivers_rankings, calculate_constructors_rankings,calculate_drivers_h2h_quali
from ressources.data_entry import get_driver_trigramme, get_driver_car_number, get_round_number, get_session_type
from ressources.constants import LOG_FILE, LOG_FORMAT, DATABASE_FILE


logger = logging.getLogger(__name__)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format=LOG_FORMAT)

def main():
    sql_connection = check_and_initialize_db(DATABASE_FILE)
    logger.info("Program ready to run")

    # Importing previous results
    print(f'Importing results for round 01')
    add_results("ROUND 1 - Q1.csv",1,"Q1",sql_connection)
    add_results("ROUND 1 - Q2.csv",1,"Q2",sql_connection)
    add_results("ROUND 1 - Q3.csv",1,"Q3",sql_connection)
    add_results("ROUND 1 - Race.csv",1,"Race",sql_connection)
    mark_round_done(sql_connection,1)
    print(f'Calculating Drivers Rankings after round 01')
    calculate_drivers_rankings(sql_connection,1)
    print(f'Calculating Constructors Rankings after round 01')
    calculate_constructors_rankings(sql_connection,1)
    print(f'Importing results for round 02')
    add_results("ROUND 2 - SQ1.csv",2,"SQ1",sql_connection)
    add_results("ROUND 2 - SQ2.csv",2,"SQ2",sql_connection)
    add_results("ROUND 2 - SQ3.csv",2,"SQ3",sql_connection)
    add_results("ROUND 2 - Sprint.csv",2,"Sprint",sql_connection)
    add_results("ROUND 2 - Q1.csv",2,"Q1",sql_connection)
    add_results("ROUND 2 - Q2.csv",2,"Q2",sql_connection)
    add_results("ROUND 2 - Q3.csv",2,"Q3",sql_connection)
    add_results("ROUND 2 - Race.csv",2,"Race",sql_connection)
    mark_round_done(sql_connection,2)
    print(f'Calculating Drivers Rankings after round 02')
    calculate_drivers_rankings(sql_connection,2)
    print(f'Calculating Constructors Rankings after round 02')
    calculate_constructors_rankings(sql_connection,2)
    print(f'Importing results for round 03')
    add_results("ROUND 3 - Q1.csv",3,"Q1",sql_connection)
    add_results("ROUND 3 - Q2.csv",3,"Q2",sql_connection)
    add_results("ROUND 3 - Q3.csv",3,"Q3",sql_connection)
    add_results("ROUND 3 - Race.csv",3,"Race",sql_connection)
    mark_round_done(sql_connection,3)
    print(f'Calculating Drivers Rankings after round 03')
    calculate_drivers_rankings(sql_connection,3)
    print(f'Calculating Constructors Rankings after round 03')
    calculate_constructors_rankings(sql_connection,3)
    print(f'Importing results for round 04')
    add_results("ROUND 4 - Q1.csv",4,"Q1",sql_connection)
    add_results("ROUND 4 - Q2.csv",4,"Q2",sql_connection)
    add_results("ROUND 4 - Q3.csv",4,"Q3",sql_connection)
    add_results("ROUND 4 - Race.csv",4,"Race",sql_connection)
    mark_round_done(sql_connection,4)
    print(f'Calculating Drivers Rankings after round 04')
    calculate_drivers_rankings(sql_connection,4)
    print(f'Calculating Constructors Rankings after round 04')
    calculate_constructors_rankings(sql_connection,4)
    print(f'Importing results for round 05')
    add_results("ROUND 5 - Q1.csv",5,"Q1",sql_connection)
    add_results("ROUND 5 - Q2.csv",5,"Q2",sql_connection)
    add_results("ROUND 5 - Q3.csv",5,"Q3",sql_connection)
    add_results("ROUND 5 - Race.csv",5,"Race",sql_connection)
    mark_round_done(sql_connection,5)
    print(f'Calculating Drivers Rankings after round 05')
    calculate_drivers_rankings(sql_connection,5)
    print(f'Calculating Constructors Rankings after round 05')
    calculate_constructors_rankings(sql_connection,5)
    print('Pre-imports done')

    
    while True:
        print(f"\n### Welcome to F1 Stats ##")
        print(f"1. Add a Driver")
        print(f"2. Add result for a session via CSV")
        print(f"3. Get Drivers Head to Head in Qualification")
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
        elif choice == 3:
            logger.info("Option chosen: Drivers Head to Head in Qualification")
            driver1: str = get_driver_trigramme()
            driver2: str = get_driver_trigramme()
            calculate_drivers_h2h_quali(sql_connection,driver1,driver2)
        elif choice == 0:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Enter options 1 - 0")

if __name__ == "__main__":
    main()