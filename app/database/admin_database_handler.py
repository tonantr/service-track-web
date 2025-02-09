from app.database.database_handler import DatabaseHandler


class AdminDatabaseHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()

    def get_all_users(self):
        query = "SELECT user_id, username, role, email FROM users"
        return self.fetch_all(query)

    def get_total_users(self):
        query = "SELECT COUNT(*) FROM users"
        result = self.fetch_one(query)
        return result["COUNT(*)"] if result else 0