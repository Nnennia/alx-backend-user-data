#!/usr/bin/env python3
"""Ä function called filter_datum that returns  the log message obfuscated"""
import logging
import mysql.connector
import os
import re


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def splitter(message, separator):
    return message.split(separator)


def pattern_replacement(field, redaction):
    pattern = r"\b" + field + r"=[^;]*"
    replacement = field + "=" + redaction
    return pattern, replacement


def filter_datum(fields, redaction, message, separator):
    message_parts = splitter(message, separator)
    for field in fields:
        pattern, replacement = pattern_replacement(field, redaction)
        for idx, val in enumerate(message_parts):
            message_parts[idx] = re.sub(pattern, replacement, val)
    return separator.join(message_parts)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION, message,
                            self.SEPARATOR)


def get_logger():
    this_logger = logging.Logger("user_data", level=logging.INFO)
    this_logger.propagate = False
    stream_handler = logging.StreamHandler(stream=None)
    log_formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(log_formatter)
    this_logger.addHandler(stream_handler)
    return this_logger


def get_db():
    """Connect to a db to read a db table"""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    data_base = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(host=db_host, database=data_base,
                                   user=username, password=password)


def main():
    with get_db() as db:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM users;")
            fields = cursor.column_names
            for row in cursor:
                message = ";".join("{}={}".format(k, v) for k,
                                   v in zip(fields, row))
                message = message.strip()
                get_logger().info(message)


if __name__ == "__main__":
    main()
