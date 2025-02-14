import logging
import os
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
                return db.fetch_one(query, (username,))
        except Exception as e:
            logging.error(f"Error in get_user_by_username: {e}")
            raise Exception(f"An error occurred while loading the user: {str(e)}")

    def get_user_by_id(self, user_id):
        try:
            query = "SELECT * FROM users WHERE user_id = %s"
            with self.db_handler as db:
                return db.fetch_one(query, (user_id,))
        except Exception as e:
            logging.error(f"Error in get_user_by_id: {e}")
            raise Exception(f"An error occurred while loading the user: {str(e)}")

    def get_car_by_id(self, car_id):
        try:
            query = "SELECT * FROM cars WHERE car_id = %s"
            with self.db_handler as db:
                return db.fetch_one(query, (car_id,))
        except Exception as e:
            logging.error(f"Error in get_car_by_id: {e}")
            raise Exception(f"An error occurred while loading the car: {str(e)}")

    def get_service_by_id(self, service_id):
        try:
            query = "SELECT * FROM services WHERE service_id = %s"
            with self.db_handler as db:
                return db.fetch_one(query, (service_id,))
        except Exception as e:
            logging.error(f"Error in get_service_by_id: {e}")
            raise Exception(f"An error occurred while loading the service: {str(e)}")

    @staticmethod
    def check_admin_session():
        if "username" not in session or session.get("role") != "admin":
            flash(ERROR_PLEASE_LOG_IN, "error")
            return False
        return True
    
    @staticmethod
    def check_user_session():
        if "username" not in session or session.get("role") not in ["admin", "user"]:
            flash(ERROR_PLEASE_LOG_IN, "error")
            return False
        return True

    def check_if_username_or_email_exists(self, username, email, exclude_user_id=None):
        try:
            query = "SELECT COUNT(*) FROM users WHERE username = %s OR email = %s"

            if exclude_user_id:
                query += " AND user_id != %s"
                with self.db_handler as db:
                    result = db.fetch_one(query, (username, email, exclude_user_id))
            else:
                with self.db_handler as db:
                    result = db.fetch_one(query, (username, email))

            if result["COUNT(*)"] > 0:
                return True
            return False
        except Exception as e:
            logging.error(f"Error in check_if_username_or_email_exists: {e}")
            raise Exception(f"An error occurred while checking username/email existence: {str(e)}")
    
    def check_vin_exists(self, vin):
        try:
            query = "SELECT COUNT(*) FROM cars WHERE vin = %s"
            with self.db_handler as db:
                result = db.fetch_one(query, (vin,))
                if result["COUNT(*)"] > 0:
                    return True
            return False
        except Exception as e:
            logging.error(f"Error in check_vin_exists: {e}")
            raise Exception(f"An error occurred while checking the vin: {str(e)}")
    
    def update_password(self, username, hashed_password):
        try:
            query = "UPDATE users SET password = %s WHERE username = %s"
            with self.db_handler as db:
                db.execute_commit(query, (hashed_password, username))
        except Exception as e:
            logging.error(f"Error in check_vin_exists: {e}")
            raise Exception(f"An error occurred while checking the vin: {str(e)}")
    
    def get_downloads_folder(self):
        if os.name == "nt":  # Windows
            return os.path.join(os.environ["USERPROFILE"], "Downloads")
        else:  # macOS/Linux
            return os.path.join(os.path.expanduser("~"), "Downloads")