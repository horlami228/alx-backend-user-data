#!/usr/bin/env python3

"""This module is for encryting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted hashed password"""

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
