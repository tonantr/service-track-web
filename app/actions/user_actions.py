import logging
from app.utils.constants import ERROR_NO_USERS_FOUND, ERROR_NO_CARS_FOUND, ERROR_NO_SERVICES_FOUND
from app.database.admin_database_handler import AdminDatabaseHandler


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


class UserActions:
    def __init__(self):
        self.admin_db_handler = AdminDatabaseHandler()