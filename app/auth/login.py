import getpass
import logging
from flask import session
from app.auth.password_hashing import verify_password, is_password_plaintext, hash_password
from app.utils.helpers import Helpers

logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


class Login:
    def __init__(self, helpers: Helpers):
        self.helpers = helpers
        self.role = None

    def authenticate(self, username, password):
        try:
            user = self.helpers.get_user_by_username(username)
            
            if user:
                stored_password = user["password"]
                if is_password_plaintext(stored_password):
                    hashed_password = hash_password(stored_password)
                    self.helpers.update_password(username, hashed_password)
                    stored_password = hashed_password

                if verify_password(password, stored_password):
                    session["username"] = username
                    self.role = user["role"]
                    session["user_id"] = user["user_id"]
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            logging.error(f"Error in authenticate: {e}")
            print("\nAn error occurred while authenticating.")
