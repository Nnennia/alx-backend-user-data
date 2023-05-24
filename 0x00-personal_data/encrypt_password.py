#!/usr/bin/env python3
"""A function that expects one string argument password and return
a salted, hashed password, which is a byte string."""
import bcrypt

def hash_password(password: str) -> bytes:
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())
