import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def create_record(user_id, segment, questions_answers , deal_id):
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO poll_table2 (user_id, deal_id, segment, questions_answers)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (str(user_id), str(deal_id) , str(segment), questions_answers))
            connection.commit()
            connection.close()
            return "Record created successfully."
    except Exception as e:
        print("An error occurred while connecting to the database:", e)


def create_table():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS poll_table2 (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR(255) NOT NULL,
                    deal_id VARCHAR(255) NOT NULL,
                    segment VARCHAR(255) NOT NULL,
                    questions_answers VARCHAR(1000) NOT NULL
                )
            """)
            connection.commit()
            connection.close()
            return "Table created successfully."
    except Exception as e:
        print("An error occurred while connecting to the database:", e)


def take_deal_id(user_id):
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT deal_id FROM poll_table2 WHERE user_id = %s;
            """, (str(user_id),))

            result = cursor.fetchall()
            connection.close()

            if result:
                return result[-1][0]
            else:
                return None

    except Exception as e:
        print("An error occurred while connecting to the database:", e)
