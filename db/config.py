from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)

DATABASE_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

pg_url = os.getenv("DB_URL")
