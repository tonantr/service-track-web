from app.database.database_handler import DatabaseHandler
from app.utils.constants import ERROR_NO_FIELDS
import logging


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)

class UserDatabaseHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()