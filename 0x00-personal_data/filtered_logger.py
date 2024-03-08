#!/usr/bin/env python3

"""This module is for logs"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obsfucated"""
    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in logs using filer_datum"""

        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """returns a logging object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to a database"""

    connection = mysql.connector.connection.MySQLConnection(
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME', 'root'),
        user=os.getenv('PERSONAL_DATA_DB_USERNAME'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    )

    return connection


def main():
    """function that returns a database connection
        and retrieve all users and display in a filterd format
    """

    db = get_db()
    cursor = db.cursor()
    logger = get_logger()
    cursor.execute("SELECT * FROM users;")

    feild_names = [i[0] for i in cursor.description]

    for row in cursor:
        full_str = "".join(f"{f}={str(r)};" for r,
                           f in zip(row, feild_names))
        logger.info(full_str)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
