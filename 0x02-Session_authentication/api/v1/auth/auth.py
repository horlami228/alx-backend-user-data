#!/usr/bin/env python3

""" Module of Auth views"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """Auth class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication"""

        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None or request.headers.get('Authorization') is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""

        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""

        if request is None:
            return None

        cookie_name = os.getenv("SESSION_NAME")

        return request.cookies.get(cookie_name)
