import logging
from flask import session
from bcrypt import hashpw, gensalt, checkpw
from app.utils.helpers import Helpers

logging.basicConfig(
    filename="app.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(module)s - Line: %(lineno)d - %(message)s",
)


def hash_password(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)
    return hashed_password.decode("utf-8")


def verify_password(password, hashed_password):
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def is_password_plaintext(password):
    return len(password) < 60


def authenticate(username, password, helpers: Helpers):
    try:
        user = helpers.get_user_by_username(username)

        if user:
            stored_password = user["password"]
            if is_password_plaintext(stored_password):
                hashed_password = hash_password(stored_password)
                helpers.update_password(username, hashed_password)
                stored_password = hashed_password

            if verify_password(password, stored_password):
                session["username"] = username
                session["role"] = user["role"]
                session["user_id"] = user["user_id"]
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        logging.error(f"Error in authenticate: {e}")
        print("\nAn error occurred while authenticating.")
