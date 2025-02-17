import os
from dotenv import load_dotenv

# Sicherstellen, dass config.env geladen wird
env_path = "/root/eventbot/config.env"
load_dotenv(env_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}