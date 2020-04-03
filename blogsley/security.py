import os
import hashlib


def generate_password_hash(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return (salt, key)

def check_password_hash(password, salt, key):
    # Use the exact same setup you used to generate the key, but this time put in the password to check
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'), # Convert the password to bytes
        salt, 
        100000
    )
    success = False
    if new_key == key:
        success = True
        print('Password is correct')
    else:
        print('Password is incorrect')
    return success
