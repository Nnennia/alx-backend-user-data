#!/usr/bin/env python3
"""
API Authentication
"""
from flask import request
from typing import TypeVar, List


class Auth:
    """ API authentication Class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False """
        if path is None or excluded_paths is None or excluded_paths == []:
            # print("I stayed here all along!")
            return True

        if path[-1] != '/':
            path = path + '/'

        for pat in excluded_paths:
            if pat[-1] == '*':
                bench_mark = len(pat) - 1
                if path[0:bench_mark] == pat[0:bench_mark]:
                    # print(pat)
                    # print("I got here")
                    return False
        # print("I passed the loop")
        return True

    def authorization_header(self, request=None) -> str:
        """ returns header request """
        if request is None:
            return None

        authorized = request.headers.get('Authorization')
        if authorized is None:
            return None

        return authorized

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None """
        return None
