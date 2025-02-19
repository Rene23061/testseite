import sqlite3

DB_PATH = "/root/eventbot/eventbot.db"

def get_db_connection():
    """Erstellt eine Verbindung zur SQLite-Datenbank und aktiviert Foreign Keys."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")  # Sicherstellen, dass Fremdschlüssel aktiviert sind
    return conn

def add_user(user_id, group_id, is_admin):
    """Fügt einen Nutzer zur Datenbank hinzu oder aktualisiert den Admin-Status."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO users (user_id, group_id, is_admin)
            VALUES (?, ?, ?)
        """, (user_id, group_id, is_admin))
        conn.commit()

def is_admin(user_id, group_id):
    """Überprüft, ob der Nutzer Admin in der Gruppe ist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT is_admin FROM users WHERE user_id = ? AND group_id = ?
        """, (user_id, group_id))
        result = cursor.fetchone()
        return result["is_admin"] if result else False

def get_group_id(user_id):
    """Ermittelt die Gruppen-ID des Nutzers oder gibt None zurück."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT group_id FROM users WHERE user_id = ?
        """, (user_id,))
        result = cursor.fetchone()
        return result["group_id"] if result else None

def add_group(group_id, owner_id, group_name):
    """Fügt eine neue Gruppe zur Datenbank hinzu, falls sie nicht existiert."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO groups (group_id, owner_id, group_name)
            VALUES (?, ?, ?)
        """, (group_id, owner_id, group_name))
        conn.commit()