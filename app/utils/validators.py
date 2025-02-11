import re


def validate_username(username):
    return len(username) >= 3


def validate_email(email):
    email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email) is not None


def validate_password(password, min_length=6):
    return len(password) >= min_length
