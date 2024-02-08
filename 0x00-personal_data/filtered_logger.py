#!/usr/bin/env python3
"""
Module for logging and obfuscating PII fields.
"""

import os
import logging
import re
import mysql.connector


class RedactingFormatter(logging.Formatter):
    """
    Formatter that redacts fields.
    """

    REDACTION = "***"
    FORMAT = ("[HOLBERTON] %(name)s %(levelname)s "
              "%(asctime)-15s: %(message)s")
    SEPARATOR = ";"

    def __init__(self, fields):
        """
        Initialize formatter.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format and redact record.
        """
        message = super().format(record)
        for field in self.fields:
            message = re.sub(f"{field}=[^;]*",
                             f"{field}={self.REDACTION}",
                             message)
        return message


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    sh = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database.
    """
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db = mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=db_name
    )
    return db


def format_log_message(fields, row):
    return '; '.join(f"{f}={str(v)}" for f, v in zip(fields, row))


def main():
    """
    Obtain a database connection using get_db
    and retrieve all rows in the users table
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    logger = get_logger()
    for row in cursor:
        logger.info(format_log_message(PII_FIELDS, row))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
