#!/usr/bin/env python3
""" Basic Authentication """
import re
import base64
from models.user import User
from typing import TypeVar
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Auth Class """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns Base64 part of the Authorization header
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        x = re.search("^Basic ", authorization_header)
        if not x:
            return None
        basic = re.split("^Basic ", authorization_header)
        return basic[-1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            value = base64_authorization_header.encode('utf-8')
            decoded_value = base64.b64decode(value)
            return decoded_value.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ returns the user email and password from
        the encoded string
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        x = re.search(':', decoded_base64_authorization_header)
        if not x:
            return (None, None)
        else:
            lst = decoded_base64_authorization_header.split(':', 1)
            email = lst[0]
            password = lst[1]
            return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on its
        email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            usr = User.search({"email": user_email})
            if not usr or usr == []:
                return None
            for user in usr:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ retrieves the User instance for a request """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            tok = self.extract_base64_authorization_header(auth_header)
            if tok is not None:
                decoded = self.decode_base64_authorization_header(tok)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                                email, password)

        return
