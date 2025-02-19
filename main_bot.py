import sqlite3

DB_PATH = "/root/eventbot/eventbot.db"

def get_db_connection():
    """Erstellt eine Verbindung zur Datenbank."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_user(user_id, group_id, is_admin):
    """Fügt einen Nutzer hinzu oder aktualisiert den Admin-Status."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO users (user_id, group_id, is_admin)
        VALUES (?, ?, ?)
    """, (user_id, group_id, is_admin))

    conn.commit()
    conn.close()

def is_admin(user_id, group_id, context):
    """Prüft zuerst in Telegram, dann in der Datenbank, ob der User Admin ist."""
    try:
        member = context.bot.get_chat_member(group_id, user_id)
        if member.status in ['administrator', 'creator']:
            return True
    except:
        pass

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE user_id = ? AND group_id = ?", (user_id, group_id))
    result = cursor.fetchone()
    conn.close()

    return result["is_admin"] if result else False

def get_group_id(user_id):
    """Gibt die Gruppen-ID eines Nutzers zurück, falls vorhanden."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result["group_id"] if result else None

def add_group(group_id, owner_id, group_name):
    """Fügt eine Gruppe zur Datenbank hinzu."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR IGNORE INTO groups (group_id, owner_id, group_name)
        VALUES (?, ?, ?)
    """, (group_id, owner_id, group_name))
    
    conn.commit()
    conn.close()