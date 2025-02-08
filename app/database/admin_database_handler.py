import logging
from app.database.database_handler import DatabaseHandler

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)

class AdminDatabaseHandler(DatabaseHandler):
    def __init__(self):
        pass