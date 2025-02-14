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
    
    def get_cars_by_user_id(self, user_id):
        try:
            with self.user_db_handler as db:
                cars = db.get_cars_by_user_id(user_id)

            if not cars:
                print(ERROR_NO_CARS_FOUND)
                return []

            return cars
        except Exception as e:
            logging.error(f"Error in get_cars_by_user_id: {str(e)}")
            return None