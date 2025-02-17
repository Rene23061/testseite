import psycopg2
from psycopg2 import sql
from src.config import DB_CONFIG

def connect_db():
    """Verbindet sich mit der Datenbank und gibt die Verbindung zurück."""
    return psycopg2.connect(**DB_CONFIG)

def add_booking(user_id, provider_id, group_id, date_time, extras=None):
    """Fügt eine neue Buchung in die Datenbank ein."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (user_id, provider_id, group_id, date_time, status, payment_status, extras_selected)
        VALUES (%s, %s, %s, %s, 'Offen', 'Offen', %s)
        RETURNING booking_id;
    """, (user_id, provider_id, group_id, date_time, extras))
    booking_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return booking_id

if __name__ == "__main__":
    print("✅ Datenbank-Funktionen bereit!")