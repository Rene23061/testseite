import psycopg2
from psycopg2 import OperationalError
from src.config import DB_CONFIG

def test_db_connection():
    """Testet die Verbindung zur PostgreSQL-Datenbank."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Verbindung zur Datenbank erfolgreich!")
        conn.close()
    except OperationalError as e:
        print(f"❌ Fehler bei der Datenbankverbindung: {e}")

# Falls die Datei direkt ausgeführt wird, testen wir die Verbindung
if __name__ == "__main__":
    test_db_connection()
