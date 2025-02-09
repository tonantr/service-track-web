import getpass
import logging
from app.auth.password_hashing import verify_password
from app.utils.helpers import Helpers

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


class Login:
    def __init__(self, helpers: Helpers):
        self.helpers = helpers
        self.logged_in_user = None
        self.role = None

    def authenticate(self, username, password):
        try:
            user = self.helpers.load_user(username)
            if user:
                stored_password = user["password"]
                if verify_password(password, stored_password):
                    self.logged_in_user = username
                    self.role = user["role"]
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            logging.error(f"Error in authenticate: {e}")
            print("\nAn error occurred while authenticating.")
