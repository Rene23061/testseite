import sqlite3

DB_PATH = "eventbot.db"

def connect_db():
    """ Erstellt eine Verbindung zur SQLite-Datenbank. """
    return sqlite3.connect(DB_PATH)

def create_tables():
    """ Erstellt alle benötigten Tabellen, falls sie nicht existieren. """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER UNIQUE NOT NULL,
            owner_id INTEGER NOT NULL,
            group_name TEXT NOT NULL,
            menu_text TEXT DEFAULT 'Willkommen beim Buchungssystem!',
            button_single TEXT DEFAULT '📅 Einzelbuchung',
            button_event TEXT DEFAULT '🎉 Event buchen',
            auto_booking BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            group_id INTEGER,
            phone_number TEXT,
            total_bookings INTEGER DEFAULT 0,
            total_cancellations INTEGER DEFAULT 0,
            vip_status BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );

        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telegram_id INTEGER NOT NULL,
            group_id INTEGER,
            pricing TEXT,
            availability TEXT,
            custom_texts TEXT,
            booking_mode TEXT CHECK (booking_mode IN ('einzeln', 'event', 'beides')),
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            provider_id INTEGER,
            group_id INTEGER,
            date_time TEXT NOT NULL,
            status TEXT CHECK (status IN ('Bestätigt', 'Offen', 'Abgesagt')),
            payment_status TEXT CHECK (payment_status IN ('Bezahlt', 'Offen')),
            extras_selected TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (provider_id) REFERENCES providers(id),
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );
    """)

    conn.commit()
    conn.close()

def get_menu_text(group_id):
    """ Holt Begrüßungstext und Button-Beschriftungen für eine Gruppe. """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT menu_text, button_single, button_event FROM groups WHERE group_id = ?
    """, (group_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result
    return ("Willkommen! Wähle eine Option:", "📅 Einzelbuchung", "🎉 Event buchen")

def add_user(telegram_id, group_id):
    """ Fügt einen neuen Benutzer hinzu, wenn er noch nicht existiert. """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, group_id, total_bookings, total_cancellations, vip_status) 
        VALUES (?, ?, 0, 0, FALSE)
        ON CONFLICT(telegram_id) DO NOTHING;
    """, (telegram_id, group_id))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("✅ SQLite-Datenbank ist bereit!")