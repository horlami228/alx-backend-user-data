#!/usr/bin/env python3

""" Module of Auth views"""
from api.v1.auth.auth import Auth


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
