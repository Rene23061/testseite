import sqlite3

# Datenbankverbindung herstellen
def connect_db():
    return sqlite3.connect("eventbot.db")

# Tabelle für Gruppen erstellen
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_group_id INTEGER UNIQUE NOT NULL,
        group_name TEXT NOT NULL,
        owner_id INTEGER NOT NULL,
        menu_text TEXT DEFAULT 'Willkommen! Was möchtest du buchen?',
        button_single TEXT DEFAULT 'Einzeltermin',
        button_event TEXT DEFAULT 'Event buchen',
        image_url TEXT DEFAULT 'none'
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL,
        group_id INTEGER,
        is_admin BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (group_id) REFERENCES groups(group_id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        group_id INTEGER NOT NULL,
        booking_type TEXT CHECK(booking_type IN ('single', 'event')),
        status TEXT CHECK(status IN ('pending', 'confirmed', 'canceled')),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (group_id) REFERENCES groups(group_id)
    );
    """)

    conn.commit()
    conn.close()

# Neuen Benutzer hinzufügen
def add_user(telegram_id, group_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO users (telegram_id, group_id)
    VALUES (?, ?)
    ON CONFLICT (telegram_id) DO NOTHING;
    """, (telegram_id, group_id))

    conn.commit()
    conn.close()

# Prüfen, ob ein Benutzer Admin ist
def is_admin(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT is_admin FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else False

# Menü-Text und Button-Namen abrufen
def get_menu_text(group_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT menu_text, button_single, button_event, image_url FROM groups WHERE group_id = ?", (group_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result if result else ("Willkommen! Was möchtest du buchen?", "Einzeltermin", "Event buchen", "none")

# Adminstatus setzen
def set_admin(telegram_id, status=True):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET is_admin = ? WHERE telegram_id = ?", (status, telegram_id))
    conn.commit()
    conn.close()

# Initiale Tabellen erstellen
create_tables()