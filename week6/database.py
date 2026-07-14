import mysql.connector

from config import DB_CONFIG


def get_database_connection():
    return mysql.connector.connect(**DB_CONFIG)
