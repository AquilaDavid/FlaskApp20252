import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5434"),
        dbname=os.getenv("POSTGRES_DB", "censoescolar"),
        user=os.getenv("POSTGRES_USER", "pweb2"),
        password=os.getenv("POSTGRES_PASSWORD", "123456")
    )
