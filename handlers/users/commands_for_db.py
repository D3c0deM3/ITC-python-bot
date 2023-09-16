import psycopg2
from psycopg2 import sql

from data.config import DB_NAME, DB_PASS, DB_HOST, DB_USER


def create_table():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()
    create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            full_name TEXT,
            phone_number TEXT,
            id_code TEXT UNIQUE,
            school TEXT,
            tuman TEXT,
            chat_id BIGINT,
            rating INTEGER,
            levels JSONB
        )
    """

    cursor.execute(create_table_query)

    conn.commit()
    cursor.close()
    conn.close()


def get_all_chat_ids():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    select_chat_ids_query = """
        SELECT chat_id FROM users
    """

    cursor.execute(select_chat_ids_query)
    result = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return [row[0] for row in result]


def insert_user_data(full_name, phone_number, id_code, tuman, school, chat_id, rating):
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    insert_user_query = """
        INSERT INTO users (full_name, phone_number, id_code, tuman, school, chat_id, rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_user_query, (full_name, phone_number, id_code, tuman, school, chat_id, rating))

    conn.commit()
    cursor.close()
    conn.close()


def create_tests_table():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )

        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS tests(
                id SERIAL PRIMARY KEY,
                test_level INTEGER,
                test_number INTEGER,
                test_photo TEXT[],
                test_video TEXT[],
                test_document TEXT[],
                test_description TEXT
            );
        """)

        conn.commit()
        print("Table 'tests' created successfully.")

    except psycopg2.Error as e:
        print(f"Error while creating table: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")



