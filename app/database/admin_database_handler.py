from app.database.database_handler import DatabaseHandler
from app.utils.constants import ERROR_NO_FIELDS
import logging


logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)

class AdminDatabaseHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def get_all_users(self):
        query = "SELECT user_id, username, role, email FROM users"
        return self.fetch_all(query)

    def add_user(self, username, email, password, role="user"):
        query = "INSERT INTO users (username, password, email, role) VALUES (%s, %s, %s, %s)"
        return self.execute_commit(query, (username, password, email, role))

    def update_user(self, user_id, **kwargs):
        if not kwargs:
            raise ValueError(ERROR_NO_FIELDS)
        
        if "role" not in kwargs:
            kwargs["role"] = "user"

        if not kwargs.get("password"):
            kwargs.pop("password", None)
        
        fields = []
        values = []

        for key, value in kwargs.items():
            fields.append(f"{key}=%s")
            values.append(value)

        query = f"UPDATE users SET {','.join(fields)} WHERE user_id=%s"
        values.append(user_id)

        return self.execute_commit(query, tuple(values))

    def delete_user(self, user_id):
        query_services = "DELETE FROM services WHERE car_id IN (SELECT car_id FROM cars WHERE user_id = %s)"
        if not self.execute_commit(query_services, (user_id,)):
            return False
        
        query_cars = "DELETE FROM cars WHERE user_id = %s"
        if not self.execute_commit(query_cars, (user_id,)):
            return False
       
        query_user = "DELETE FROM users WHERE user_id = %s"
        if not self.execute_commit(query_user, (user_id,)):
            return False
        
        return True

    def get_all_cars(self):
        query = """
            SELECT 
            c.car_id, 
            c.name, 
            c.model, 
            c.year,
            c.vin, 
            u.username AS owner
        FROM cars c
        LEFT JOIN users u ON c.user_id = u.user_id
        ORDER BY c.car_id;  
        """
        return self.fetch_all(query)

    def add_car(self, **kwargs):
        if not kwargs:
            raise ValueError(ERROR_NO_FIELDS)
        
        fields = []
        values = []

        for key, value in kwargs.items():
            fields.append(key)
            values.append(value)
        
        query = f"INSERT INTO cars ({','.join(fields)}) VALUES ({','.join(['%s'] * len(values))})"
        
        return self.execute_commit(query, tuple(values))
    
    def update_car(self, car_id, **kwargs):
        if not kwargs:
            raise ValueError(ERROR_NO_FIELDS)
        
        fields = []
        values = []

        for key, value in kwargs.items():
            fields.append(f"{key}=%s")
            values.append(value)
        
        query = f"UPDATE cars SET {','.join(fields)} WHERE car_id = %s"
        values.append(car_id)
        return self.execute_commit(query, tuple(values))

    def delete_car(self, car_id):
        query_services = "DELETE FROM services WHERE car_id = %s"
        if not self.execute_commit(query_services, (car_id,)):
            return False
        
        query_cars = "DELETE FROM cars WHERE car_id = %s"
        if not self.execute_commit(query_cars, (car_id,)):
            return False
        
        return True

    def get_all_services(self):
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
            ORDER BY s.service_date ASC, s.next_service_date ASC;
        """
        return self.fetch_all(query)
    
    def add_service(self, **kwargs):
        if not kwargs:
            raise ValueError(ERROR_NO_FIELDS)
        
        fields = list(kwargs.keys())
        values = list(kwargs.values())

        query = f"INSERT INTO services ({','.join(fields)}) VALUES ({', '.join(['%s'] * len(fields))})"
        return self.execute_commit(query, tuple(values))

    def update_service(self, service_id, **kwargs):
        if not kwargs:
            raise ValueError(ERROR_NO_FIELDS)
        
        fields = [f"{key} = %s" for key in kwargs.keys()]
        values = list(kwargs.values())

        query = f"UPDATE services SET {', '.join(fields)} WHERE service_id = %s"
        values.append(service_id)
        return self.execute_commit(query, tuple(values))
    
    def delete_service(self, service_id):
        query_services = "DELETE FROM services WHERE service_id = %s"
        if not self.execute_commit(query_services, (service_id,)):
            return False
        
        return True

    def get_total_users(self):
        query = "SELECT COUNT(*) FROM users"
        result = self.fetch_one(query)
        return result["COUNT(*)"] if result else 0

    def get_total_cars(self):
        query = "SELECT COUNT(*) FROM cars"
        result = self.fetch_one(query)
        return result["COUNT(*)"] if result else 0
    
    def get_total_services(self):
        query = "SELECT COUNT(*) FROM services"
        result = self.fetch_one(query)
        return result["COUNT(*)"] if result else 0