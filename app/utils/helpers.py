import logging
from app.database.database_handler import DatabaseHandler
from app.utils.constants import ERROR_PLEASE_LOG_IN
from flask import flash, session


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


class Helpers:
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    def load_user(self, username):
        try:
            query = "SELECT * FROM users WHERE username = %s"
            with self.db_handler as db:
                user = db.fetch_one(query, (username,))
                if not user:
                    return None
                return user
        except Exception as e:
            logging.error(f"Error in load_user: {e}")
            raise Exception(f"An error occurred while loading the user: {str(e)}")

    def check_admin_session(self):
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return False
        return True