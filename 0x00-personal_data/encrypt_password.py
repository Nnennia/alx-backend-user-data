#!/usr/bin/env python3
"""A function that expects one string argument password and return
a salted, hashed password, which is a byte string."""
import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password"""
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches
    the hashed password using bcrypt."""
    password = password.encode()
    return bcrypt.checkpw(password, hashed_password)
