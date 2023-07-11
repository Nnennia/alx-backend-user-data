#!/usr/bin/env python3
""" Authentication """
import bcrypt
import uuid
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
from user import User


def _hash_password(password: str) -> str:
    """ takes in a password string
    arg and returns bytes
    """
    byte = password.encode('utf-8')

    salt = bcrypt.gensalt()

    return (bcrypt.hashpw(byte, salt))


def _generate_uuid() -> str:
    """ returns a string representation
    of a new UUID.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers a new user """
        try:
            find_user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)

            return new_user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """ validate credentials """
        try:
            find_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'),
                              find_user.hashed_password)

    def create_session(self, email: str) -> str:
        """ takes an email string argument and
        returns the session ID as a string.
        """
        try:
            find_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(find_user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ takes a single session_id string
        argument and returns the corresponding User
        or None
        """
        if session_id is None:
            return None
        try:
            find_user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        else:
            return find_user

    def destroy_session(self, user_id: int) -> None:
        """ takes a single user_id integer argument
        and returns None
        """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ take an email string argument and
        returns a string
        """
        try:
            find_user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        else:
            reset_token = _generate_uuid()
            self._db.update_user(find_user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ takes reset_token string argument and a
        password string argument and returns None
        """
        try:
            find_user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        else:
            hashed_password = _hash_password(password)
            self._db.update_user(find_user.id,
                                 hashed_password=hashed_password,
                                 reset_token=None)
