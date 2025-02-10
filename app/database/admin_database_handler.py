from app.database.database_handler import DatabaseHandler
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

    def update_user(self, user_id, **kwargs):
        if not kwargs:
            raise ValueError("No fields to update")
        
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

        self.execute_commit(query, tuple(values))

    def get_all_cars(self):
        query = """
            SELECT 
            c.car_id, 
            c.name, 
            c.model, 
            c.year, 
            u.username AS owner
        FROM cars c
        LEFT JOIN users u ON c.user_id = u.user_id
        ORDER BY c.car_id;  
        """
        return self.fetch_all(query)

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