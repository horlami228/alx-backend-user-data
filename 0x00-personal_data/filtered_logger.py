#!/usr/bin/env python3

"""This module is for logs"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """returns the log message obsfucated"""
    for field in fields:
        message = re.sub(rf"{field}=.*?{seperator}",
                         rf"{field}={redaction}{seperator}", message)
    return message
