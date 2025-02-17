import os
from dotenv import load_dotenv

load_dotenv("config.env")  # Lädt jetzt config.env statt .env

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}
