import sqlite3

DB_PATH = "/root/eventbot/database.sqlite3"

def connect_db():
    """ Erstellt eine Verbindung zur SQLite-Datenbank. """
    return sqlite3.connect(DB_PATH)

def create_tables():
    """ Erstellt die benötigten Tabellen, falls sie nicht existieren. """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            group_id INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            group_id INTEGER PRIMARY KEY,
            group_name TEXT NOT NULL,
            menu_text TEXT DEFAULT 'Willkommen!',
            button_single TEXT DEFAULT 'Einzelbuchung',
            button_event TEXT DEFAULT 'Event buchen',
            image_path TEXT DEFAULT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE NOT NULL,
            group_id INTEGER NOT NULL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def get_menu_text(group_id):
    """ Holt den Begrüßungstext, Buttons & Bild für eine Gruppe. """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT menu_text, button_single, button_event, image_path FROM groups WHERE group_id = ?
    """, (group_id,))
    
    result = cursor.fetchone()
    
    if result:
        return result
    else:
        return "Willkommen!", "Einzelbuchung", "Event buchen", None

def add_user(telegram_id, group_id):
    """ Fügt einen neuen Nutzer zur Datenbank hinzu, falls nicht vorhanden. """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (telegram_id, group_id) VALUES (?, ?)
    """, (telegram_id, group_id))

    conn.commit()
    cursor.close()
    conn.close()

def is_admin(telegram_id, group_id):
    """ Prüft, ob der Nutzer Admin ist. """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 1 FROM admins WHERE telegram_id = ? AND group_id = ?
    """, (telegram_id, group_id))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result is not None

# Tabellen erstellen beim Start
create_tables()
print("✅ SQLite-Datenbank ist bereit!")