import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def init_db():
    connect()
    create_tables()


def connect():
    """Establishes a connection to the PostgreSQL database."""
    host = os.getenv("POSTGRES_HOST")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")

    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        print("Connection to the database successful.")
        return connection

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        raise e


def create_tables():
    """Reads and executes the SQL commands to create tables."""
    connection = connect()
    if connection is None:
        return

    tables = {
        "records": "create_table_records.sql"
    }

    try:
        with connection.cursor() as cursor:
            for table_name, file_name in tables.items():
                # Get the path to the current script's directory
                script_dir = os.path.dirname(__file__)
                # Construct the path to the SQL file inside the 'sql' subdirectory
                sql_file_path = os.path.join(script_dir, "sql", file_name)

                # Read SQL commands from the file and execute them
                with open(sql_file_path, "r") as sql_file:
                    create_table_sql = sql_file.read()

                cursor.execute(create_table_sql)
                connection.commit()
                print(f"Table '{table_name}' created successfully.")

    except (psycopg2.Error, FileNotFoundError) as e:
        print("Error creating tables:", e)

    finally:
        connection.close()
