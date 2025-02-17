import psycopg2
from psycopg2 import sql
from src.config import DB_CONFIG

def connect_db():
    """Stellt eine Verbindung zur PostgreSQL-Datenbank her."""
    return psycopg2.connect(**DB_CONFIG)

# 📌 Nutzer hinzufügen (wenn noch nicht vorhanden)
def add_user(telegram_id, group_id):
    """Fügt einen neuen Nutzer hinzu oder ignoriert ihn, wenn er bereits existiert."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, group_id, total_bookings, total_cancellations, vip_status) 
        VALUES (%s, %s, 0, 0, FALSE) 
        ON CONFLICT (telegram_id, group_id) DO NOTHING;
    """, (telegram_id, group_id))
    conn.commit()
    cursor.close()
    conn.close()

# 📌 Einzelbuchung speichern
def add_booking(user_id, provider_id, group_id, date_time, extras=None):
    """Speichert eine neue Einzelbuchung in der Datenbank."""
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

# 📌 Event-Buchung speichern
def add_event_booking(user_id, event_id, status):
    """Speichert eine Event-Buchung."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO event_bookings (user_id, event_id, status)
        VALUES (%s, %s, %s)
        RETURNING id;
    """, (user_id, event_id, status))
    booking_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return booking_id

# 📌 Blacklist-Eintrag hinzufügen
def add_to_blacklist(user_id, reason):
    """Fügt einen Nutzer zur globalen Blacklist hinzu."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO blacklist (user_id, reason, total_strikes)
        VALUES (%s, %s, 1)
        ON CONFLICT (user_id) DO UPDATE 
        SET total_strikes = blacklist.total_strikes + 1;
    """, (user_id, reason))
    conn.commit()
    cursor.close()
    conn.close()

# 📌 Erinnerungen abrufen
def get_reminder(provider_id, group_id, reminder_type):
    """Holt einen Erinnerungstext für Buchungen oder Events."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT reminder_text FROM reminders 
        WHERE provider_id = %s AND group_id = %s AND type = %s;
    """, (provider_id, group_id, reminder_type))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

if __name__ == "__main__":
    print("✅ Datenbank-Funktionen bereit!")