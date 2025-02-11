from bcrypt import hashpw, gensalt, checkpw

def hash_password(password):
    salt = gensalt()
    hashed_password = hashpw(password.encode(), salt)
    return hashed_password.decode('utf-8')

def verify_password(password, hashed_password):
    return checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))