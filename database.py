import psycopg2
from psycopg2 import sql
from src.config import DB_CONFIG

def connect_db():
    """Stellt eine Verbindung zur PostgreSQL-Datenbank her."""
    return psycopg2.connect(**DB_CONFIG)

# 📌 Nutzer speichern
def add_user(telegram_id, group_id):
    """Speichert einen neuen Nutzer oder ignoriert ihn, falls er schon existiert."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, group_id) 
        VALUES (%s, %s) 
        ON CONFLICT (telegram_id, group_id) DO NOTHING;
    """, (telegram_id, group_id))
    conn.commit()
    cursor.close()
    conn.close()

# 📌 Menü-Text & Button-Namen aus DB holen
def get_menu_text(group_id):
    """Holt den Startmenü-Text & die Button-Namen aus der Datenbank."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT menu_text, button_single, button_event FROM groups WHERE group_id = %s;
    """, (group_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result  # (menu_text, button_single, button_event)
    else:
        return ("Willkommen! Wähle deine Buchung:", "📅 Einzelbuchung", "🎉 Event-Buchung")

# 📌 Einzelbuchung speichern
def add_booking(user_id, provider_id, group_id, date_time, extras=None):
    """Speichert eine neue Einzelbuchung."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO bookings (user_id, provider_id, group_id, date_time, status)
        VALUES (%s, %s, %s, %s, 'Offen')
        RETURNING booking_id;
    """, (user_id, provider_id, group_id, date_time))
    booking_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return booking_id

# 📌 Event-Buchung speichern
def add_event_booking(user_id, event_id):
    """Speichert eine Event-Buchung."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO event_bookings (user_id, event_id, status)
        VALUES (%s, %s, 'Bestätigt')
        RETURNING id;
    """, (user_id, event_id))
    booking_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return booking_id

if __name__ == "__main__":
    print("✅ Datenbank-Funktionen bereit!")