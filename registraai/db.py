import time
import os

from flask import g
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv

load_dotenv()

db_config = {
    "minconn": 1,
    "maxconn": 10,
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST")
}


def load_query(name: str) -> str:
    """
    Load an SQL query from a file.

    This function reads an SQL query from a file in the 'sql' directory based on the given name.

    Args:
        name (str): The name of the SQL query file (without the file extension).

    Returns:
        str: The contents of the SQL query as a string.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "sql", name)

    with open(file_path, 'r') as file:
        query = file.read()
    return query


def execute_query(query:str, values:tuple = ()) -> None|list[tuple]:
    """
    Execute an SQL query with optional parameters.

    This function executes the given SQL query with optional parameter values.

    Args:
        query (str): The SQL query to execute.
        values (tuple, optional): The parameter values for the query (default: ()).

    Returns:
        None|list[tuple]: The result of the query, either a list of tuples or
        None.
    """
    conn = g.connection_pool.getconn()
    cursor = conn.cursor()
    result = None

    try:
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        conn.commit()
        if cursor.description:
            result = cursor.fetchall()
    finally:
        cursor.close()
        g.connection_pool.putconn(conn)

    return result


def init_db(app):
    """
    Initialize the database.

    This function initializes the database by creating the connection pool and
    creating tables.

    Args:
        app: The Flask application object.
    """
    with app.app_context():
        init_pool()
        create_tables()


def init_pool():
    """
    Initialize the connection pool.

    This function initializes the connection pool for database connections.

    Raises:
        RuntimeError: If the connection to the database fails after multiple
        attempts.
    """
    if 'connection_pool' not in g:
        max_attempts = 3
        attempts = 0
        connection_pool = None

        while attempts < max_attempts:
            try:
                connection_pool = pool.SimpleConnectionPool(**db_config)
                break
            except psycopg2.OperationalError:
                attempts += 1
                wait_time = attempts  # Increase the wait time with each attempt
                print(f"Attempt {attempts}/{max_attempts}: Database not ready, waiting {wait_time} seconds...")
                time.sleep(wait_time)

        if connection_pool is None:
            raise RuntimeError("Failed to connect to the database after multiple attempts.")

        g.connection_pool = connection_pool


def create_tables():
    """
    Create database tables.

    This function creates the necessary tables in the database.

    Note:
        The SQL query for creating tables must be defined in a file named
        'create_table_records.sql' and placed in the 'sql' directory.
    """
    create_table_records_query = "create_table_records.sql"
    query = load_query(create_table_records_query)

    execute_query(query)
