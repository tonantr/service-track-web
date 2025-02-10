import logging
from app.database.database_handler import DatabaseHandler
from flask import flash, redirect

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
                return db.fetch_one(query, (username,))
        except Exception as e:
            logging.error(f"Error in load_user: {e}")
            print("\nAn error occurred while loading user.")
