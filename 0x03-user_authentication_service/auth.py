#!/usr/bin/env python3
import bcrypt


def _hash_password(password: str) -> bytes:
    """Takes in a string and returns a hash"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
