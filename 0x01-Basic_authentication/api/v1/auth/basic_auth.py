#!/usr/bin/env python3

""" Module of Auth views"""
from api.v1.auth.auth import Auth
import base64


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
            decode_byte = base64.b64decode(base64_authorization_header)
        except Exception:
            return None

        decoded_str = decode_byte.decode('utf-8')

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
