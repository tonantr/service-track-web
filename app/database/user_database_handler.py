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
    
    def get_cars_by_user(self, userid):
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
    
    def get_services_by_car(self,car_id):
        query = """
            SELECT 
                s.service_id, 
                c.name AS car_name,
                s.mileage,
                s.service_type, 
                s.service_date,
                s.next_service_date,
                s.cost,
                s.notes
            FROM services s
            LEFT JOIN cars c ON s.car_id = c.car_id
            WHERE s.car_id = %s
            ORDER BY s.service_date ASC, s.next_service_date ASC;
        """
        return self.fetch_all(query, (car_id,))