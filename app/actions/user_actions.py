import logging
from app.utils.constants import ERROR_NO_USERS_FOUND, ERROR_NO_CARS_FOUND, ERROR_NO_SERVICES_FOUND
from app.database.user_database_handler import UserDatabaseHandler


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


class UserActions:
    def __init__(self):
        self.user_db_handler = UserDatabaseHandler()
    
    def get_cars_by_user(self, user_id):
        try:
            with self.user_db_handler as db:
                cars = db.get_cars_by_user(user_id)

            if not cars:
                print(ERROR_NO_CARS_FOUND)
                return []

            return cars
        except Exception as e:
            logging.error(f"Error in get_cars_by_user_id: {str(e)}")
            return None
    
    def update_user(self, user_id, **kwargs):
        try:
            with self.user_db_handler as db:
                return db.update_user(user_id, **kwargs)
        except Exception as e:
            logging.error(f"Error in update_user: {str(e)}")
            return False

    def get_services_by_car(self, car_id):
        try:
            with self.user_db_handler as db:
                services = db.get_services_by_car(car_id)

            if not services:
                print(ERROR_NO_SERVICES_FOUND)
                return []

            return services
        except Exception as e:
            logging.error(f"Error in get_services_by_car: {str(e)}")
            return None
    
    def add_service(self, **kwargs):
        try:
            with self.user_db_handler as db:
                return db.add_service(**kwargs)
        except Exception as e:
            logging.error(f"Error in add_service: {str(e)}")
            return False
    
    def delete_service(self, service_id):
        try:
            with self.user_db_handler as db:
                return db.delete_service(service_id)
        except Exception as e:
            logging.error(f"Error in delete_service: {str(e)}")
            return False

    def update_service(self, service_id, **kwargs):
        try:
            with self.user_db_handler as db:
                return db.update_service(service_id, **kwargs)
        except Exception as e:
            logging.error(f"Error in update_service: {str(e)}")
            return None

    def update_car(self, car_id, **kwargs):
        try:
            with self.user_db_handler as db:
                cars = db.update_car(car_id, **kwargs)
            
            if not cars:
                print(ERROR_NO_CARS_FOUND)
                return []
            
            return cars
        except Exception as e:
            logging.error(f"Error in update_car: {str(e)}")
            return None
        
    def delete_car(self, car_id):
        try:
            with self.user_db_handler as db:
                return db.delete_car(car_id)
        except Exception as e:
            logging.error(f"Error in delete_car: {str(e)}")
            return False
    
    def add_car(self, **kwargs):
        try:
            with self.user_db_handler as db:
                return db.add_car(**kwargs)
        except Exception as e:
            logging.error(f"Error in add_car: {str(e)}")
            return False