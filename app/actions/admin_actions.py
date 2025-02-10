import logging
from app.utils.constants import ERROR_NO_USERS_FOUND, ERROR_NO_CARS_FOUND, ERROR_NO_SERVICES_FOUND
from app.database.admin_database_handler import AdminDatabaseHandler


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


class AdminActions:
    def __init__(self):
        self.admin_db_handler = AdminDatabaseHandler()

    def get_all_users(self):
        try:
            with self.admin_db_handler as db:
                users = db.get_all_users()

            if not users:
                print(ERROR_NO_USERS_FOUND)
                return []

            return users
        except Exception as e:
            logging.error(f"Error in get_all_users: {str(e)}")
            return None

    def get_all_cars(self):
        try:
            with self.admin_db_handler as db:
                cars = db.get_all_cars()
            
            if not cars:
                print(ERROR_NO_CARS_FOUND)
                return []
            
            return cars
        except Exception as e:
            logging.error(f"Error in get_all_cars: {str(e)}")
            return None
    
    def get_all_services(self):
        try:
            with self.admin_db_handler as db:
                services = db.get_all_services()
            
            if not services:
                print(ERROR_NO_SERVICES_FOUND)
                return []
            
            return services
        except Exception as e:
            logging.error(f"Error in get_all_services: {str(e)}")
            return None

    def get_total_users(self):
        try:
            with self.admin_db_handler as db:
                return db.get_total_users()
        except Exception as e:
            logging.error(f"Error in get_total_users: {str(e)}")
            return None

    def get_total_cars(self):
        try:
            with self.admin_db_handler as db:
                return db.get_total_cars()
        except Exception as e:
            logging.error(f"Error in get_total_cars: {str(e)}")
            return None
    
    def get_total_services(self):
        try:
            with self.admin_db_handler as db:
                return db.get_total_services()
        except Exception as e:
            logging.error(f"Error in get_total_services: {str(e)}")
            return None