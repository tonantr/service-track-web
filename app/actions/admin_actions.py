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

    def add_user(self, username, email, password, role):
        try:
            with self.admin_db_handler as db:
                return db.add_user(username, email, password, role)
        except Exception as e:
            logging.error(f"Error in add_user: {str(e)}")
            return False

    def update_user(self, user_id, **kwargs):
        try:
            with self.admin_db_handler as db:
                return db.update_user(user_id, **kwargs)
        except Exception as e:
            logging.error(f"Error in update_user: {str(e)}")
            return False
    
    def delete_user(self, user_id):
        try:
            with self.admin_db_handler as db:
                return db.delete_user(user_id)
        except Exception as e:
            logging.error(f"Error in delete_user: {str(e)}")
            return False

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
    
    def add_car(self, **kwargs):
        try:
            with self.admin_db_handler as db:
                return db.add_car(**kwargs)
        except Exception as e:
            logging.error(f"Error in add_car: {str(e)}")
            return False

    def update_car(self, car_id, **kwargs):
        try:
            with self.admin_db_handler as db:
                return db.update_car(car_id, **kwargs)
        except Exception as e:
            logging.error(f"Error in update_car: {str(e)}")
            return False

    def delete_car(self, car_id):
        try:
            with self.admin_db_handler as db:
                return db.delete_car(car_id)
        except Exception as e:
            logging.error(f"Error in delete_car: {str(e)}")
            return False

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