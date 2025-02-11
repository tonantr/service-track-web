import mysql.connector
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


class DatabaseHandler:
    def __init__(self, host=None, user=None, password=None, database=None):
        self.host = host or os.getenv("MYSQL_HOST_WINDOWS")
        self.user = user or os.getenv("MYSQL_USER")
        self.password = password or os.getenv("MYSQL_PASSWORD")
        self.database = database or os.getenv("MYSQL_DATABASE")
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as e:
            logging.error(f"Connection Error: {str(e)}")
            raise

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except mysql.connector.Error as e:
            logging.error(f"Close Error: {str(e)}")
            raise

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        if exc_type:
            logging.error(f"Error: {exc_value}")
        return True

    def fetch_all(self, query, params=None):
        # Execute a query and return the result
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            logging.error(f"Query Error: {str(e)} | Query: {query} | Params: {params}")
            raise

    def execute_commit(self, query, params=None):
        # Execute a query and commit the changes (e.g. INSERT, UPDATE, DELETE)
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            logging.error(f"Commit Error: {str(e)} | Query: {query} | Params: {params}")
            raise

    def fetch_one(self, query, params=None):
        # Fetch a single row from a query
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            logging.error(f"Fetch Error: {str(e)} | Query: {query} | Params: {params}")
            raise
