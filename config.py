import os
from dotenv import load_dotenv

# Lade config.env aus /root/eventbot/
load_dotenv("/root/eventbot/config.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}