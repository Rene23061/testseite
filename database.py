import sqlite3

DB_PATH = "/root/eventbot/eventbot.db"

def get_db_connection():
    """Erstellt und gibt eine Verbindung zur Datenbank zurück."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    """Erstellt die notwendigen Tabellen, falls sie nicht existieren."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER UNIQUE NOT NULL,
            owner_id INTEGER NOT NULL,
            group_name TEXT NOT NULL,
            auto_booking BOOLEAN DEFAULT FALSE,
            menu_text TEXT DEFAULT 'Willkommen!',
            button_single TEXT DEFAULT 'Einzelbuchung',
            button_event TEXT DEFAULT 'Eventbuchung'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            group_id INTEGER NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            FOREIGN KEY(group_id) REFERENCES groups(group_id)
        )
    """)

    conn.commit()
    conn.close()

def add_group(group_id, owner_id, group_name):
    """Fügt eine neue Gruppe zur Datenbank hinzu."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR IGNORE INTO groups (group_id, owner_id, group_name)
        VALUES (?, ?, ?)
    """, (group_id, owner_id, group_name))
    
    conn.commit()
    conn.close()

def add_user(user_id, group_id, is_admin=False):
    """Fügt einen Nutzer hinzu oder aktualisiert den Admin-Status."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id, group_id, is_admin)
        VALUES (?, ?, ?)
    """, (user_id, group_id, is_admin))
    
    conn.commit()
    conn.close()

def is_admin(user_id, group_id):
    """Prüft, ob ein Nutzer Admin ist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT is_admin FROM users WHERE user_id = ? AND group_id = ?
    """, (user_id, group_id))
    
    result = cursor.fetchone()
    conn.close()

    return result and result["is_admin"]

def get_group_id(user_id):
    """Holt die Gruppen-ID, mit der der Nutzer verknüpft ist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT group_id FROM users WHERE user_id = ?
    """, (user_id,))
    
    result = cursor.fetchone()
    conn.close()

    return result["group_id"] if result else None

def get_menu_text(group_id):
    """Holt den Begrüßungstext und die Button-Namen für eine Gruppe."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT menu_text, button_single, button_event FROM groups WHERE group_id = ?
    """, (group_id,))
    
    result = cursor.fetchone()
    conn.close()

    if result:
        return result["menu_text"], result["button_single"], result["button_event"]
    return "Kein Text vorhanden", "Kein Einzelbuchung", "Kein Eventbuchung"

# Sicherstellen, dass die Datenbank initialisiert ist
setup_database()