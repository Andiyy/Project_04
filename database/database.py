#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Database contextmanager."""


import sqlite3
from contextlib import contextmanager


@contextmanager
def open_sqlite3(database: str = 'database/test_reports.db'):
    """Handling the database connection.

    :param database The path to the database.
    """
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
        yield cursor
    finally:
        conn.commit()
        conn.close()
