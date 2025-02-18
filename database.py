import sqlite3

# Verbindung zur Datenbank herstellen
DB_PATH = "/root/eventbot/eventbot.db"

def get_db_connection():
    """ Erstellt eine neue Datenbankverbindung und gibt Cursor zurück. """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

def get_group_id(user_id):
    """ Ruft die group_id eines Nutzers aus der Datenbank ab. """
    conn, cursor = get_db_connection()
    
    cursor.execute("SELECT group_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else None

def add_user(user_id, group_id, is_admin=False):
    """ Fügt einen neuen Benutzer zur Datenbank hinzu, falls nicht vorhanden. """
    conn, cursor = get_db_connection()
    
    cursor.execute("INSERT OR IGNORE INTO users (user_id, group_id, is_admin) VALUES (?, ?, ?)",
                   (user_id, group_id, is_admin))
    conn.commit()
    conn.close()

def is_admin(user_id):
    """ Prüft, ob ein Benutzer ein Admin ist. """
    conn, cursor = get_db_connection()
    
    cursor.execute("SELECT is_admin FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else 0

def add_group(group_id, owner_id, group_name):
    """ Fügt eine neue Gruppe zur Datenbank hinzu, falls nicht vorhanden. """
    conn, cursor = get_db_connection()
    
    cursor.execute("INSERT OR IGNORE INTO groups (group_id, owner_id, group_name) VALUES (?, ?, ?)",
                   (group_id, owner_id, group_name))
    conn.commit()
    conn.close()