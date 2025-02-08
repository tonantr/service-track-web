from bcrypt import hashpw, gensalt, checkpw

def hash_password(password):
    return hashpw(password.encode(), gensalt)

def verify_password(password, hashed):
    return checkpw(password.encode(), hashed.encode())