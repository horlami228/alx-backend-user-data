#!/usr/bin/env python3

""" Module of Auth views"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Defines the BasicAuth class"""

    def __init__(self):
        """Initializes the BasicAuth class"""
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the base64 authorization header"""
        if authorization_header is None\
                or type(authorization_header) is not str:
            return None
        if authorization_header[0:6] != "Basic ":
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Decodes the base64 authorization header"""
        if base64_authorization_header is None\
                or type(base64_authorization_header) is not str:
            return None

        try:
            decoded_str = base64.b64decode(
                base64_authorization_header).decode("utf-8")
        except Exception:
            return None

        return decoded_str

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str)\
            -> (str, str):
        """Extracts the user credentials from the
        decoded base64 authorization header"""

        if decoded_base64_authorization_header is None\
                or type(decoded_base64_authorization_header) is not str\
                or ":" not in decoded_base64_authorization_header:
            return (None, None)

        else:
            email, password = decoded_base64_authorization_header.split(":", 1)

            return (email, password)

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """Returns the User instance based on his email and password"""

        if user_email is None or user_pwd is None\
                or type(user_email) is not str or type(user_pwd) is not str:
            return None

        user = User.search({"email": user_email})

        if len(user) == 0 or not user[0].is_valid_password(user_pwd):
            return None
        else:
            return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header)
        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header)
        return self.user_object_from_credentials(user_email, user_pwd)
