import sqlite3

DB_PATH = "/root/eventbot/eventbot.db"

def get_db_connection():
    """Erstellt eine Datenbankverbindung."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_user(user_id, group_id, is_admin):
    """Fügt einen Benutzer zur Datenbank hinzu oder aktualisiert den Admin-Status."""
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

    if result:
        return result["is_admin"]
    
    return False

def get_group_id(user_id):
    """Holt die Gruppen-ID aus der Datenbank basierend auf der User-ID."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT group_id FROM users WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result["group_id"]
    
    return None

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