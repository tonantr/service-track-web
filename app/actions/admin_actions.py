import logging
from app.utils.constants import ERROR_NO_USERS_FOUND
from app.database.admin_database_handler import AdminDatabaseHandler


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


class AdminActions:
    def __init__(self):
        self.admin_db_handler = AdminDatabaseHandler()

    def list_users(self):
        try:
            with self.admin_db_handler as db:
                users = db.get_all_users()

            if not users:
                print(ERROR_NO_USERS_FOUND)
                return

            return users
        except Exception as e:
            logging.error("Error in list_users: %s", str(e))
            return []
