#!/usr/bin/env python3

"""This module is for encryting passwords"""
from bcrypt import hashpw, gensalt


def hash_password(password: str) -> bytes:
    """returns a salted hashed password"""

    return hashpw(password.encode('utf-8'), gensalt())
