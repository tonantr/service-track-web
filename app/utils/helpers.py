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

    def get_user_by_username(self, username):
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

    def get_user_by_id(self, user_id):
        try:
            query = "SELECT * FROM users WHERE user_id = %s"
            with self.db_handler as db:
                user = db.fetch_one(query, (user_id,))
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
    
    def check_if_username_or_email_exists(self, username, email):
        try:
            query = "SELECT COUNT(*) FROM users WHERE username = %s OR email = %s"
            with self.db_handler as db:
                result = db.fetch_one(query, (username, email))
                if result["COUNT(*)"] > 0:
                    return True
                return False
        except Exception as e:
            logging.error(f"Error in load_user: {e}")
            raise Exception(f"An error occurred while checking username/email existence: {str(e)}")