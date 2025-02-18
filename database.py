import sqlite3

DB_PATH = "/root/eventbot/eventbot.db"

def connect_db():
    """Stellt eine Verbindung zur SQLite-Datenbank her."""
    return sqlite3.connect(DB_PATH)

def create_tables():
    """Erstellt die notwendigen Tabellen, falls sie nicht existieren."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        group_id INTEGER UNIQUE NOT NULL,
        owner_id INTEGER NOT NULL,
        group_name TEXT NOT NULL,
        auto_booking BOOLEAN DEFAULT FALSE
    );

    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL,
        group_id INTEGER REFERENCES groups(id),
        phone_number TEXT,
        total_bookings INTEGER DEFAULT 0,
        total_cancellations INTEGER DEFAULT 0,
        vip_status BOOLEAN DEFAULT FALSE,
        UNIQUE (telegram_id, group_id)
    );

    CREATE TABLE IF NOT EXISTS providers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        telegram_id INTEGER NOT NULL,
        group_id INTEGER REFERENCES groups(id),
        pricing TEXT,
        availability TEXT,
        custom_texts TEXT,
        booking_mode TEXT CHECK (booking_mode IN ('einzeln', 'event', 'beides'))
    );

    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(id),
        provider_id INTEGER REFERENCES providers(id),
        group_id INTEGER REFERENCES groups(id),
        date_time TEXT NOT NULL,
        status TEXT CHECK (status IN ('Bestätigt', 'Offen', 'Abgesagt')),
        payment_status TEXT CHECK (payment_status IN ('Bezahlt', 'Offen')),
        extras_selected TEXT
    );

    CREATE TABLE IF NOT EXISTS blacklist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER REFERENCES users(id),
        date_added TEXT DEFAULT CURRENT_TIMESTAMP,
        reason TEXT,
        total_strikes INTEGER DEFAULT 1
    );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ SQLite-Datenbank ist bereit!")

def get_menu_text(group_id):
    """Holt das Menü für eine bestimmte Telegram-Gruppe."""
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT group_name FROM groups WHERE group_id = ?;
    """, (group_id,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else ("Willkommen!", "Einzelbuchung", "Party/Event")

create_tables()