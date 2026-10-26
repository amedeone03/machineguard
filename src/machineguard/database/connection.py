import os

import psycopg


def get_connection():
    return psycopg.connect(
        dbname=os.getenv(
            "DB_NAME",
            "machineguard",
        ),
        user=os.getenv(
            "DB_USER",
            None,
        ),
        password=os.getenv(
            "DB_PASSWORD",
            None,
        ),
        host=os.getenv(
            "DB_HOST",
            None,
        ),
        port=os.getenv(
            "DB_PORT",
            "5432",
        ),
    )