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
    
    def get_cars_by_user_id(self, userid):
        query = """
        SELECT car_id, user_id, name, model, year, vin 
        FROM cars 
        WHERE user_id = %s
        """
        return self.fetch_all(query, (userid,))
    
    def update_user(self, user_id, **kwargs):
        if not kwargs:
            raise ValueError(ERROR_NO_FIELDS)

        if not kwargs.get("password"):
            kwargs.pop("password", None)
        
        fields = [f"{key}=%s" for key in kwargs.keys()]
        values = list(kwargs.values())

        query = f"UPDATE users SET {','.join(fields)} WHERE user_id=%s"
        values.append(user_id)

        return self.execute_commit(query, tuple(values))