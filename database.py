import sqlite3

DB_PATH = "/root/eventbot/eventbot.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_user(user_id, group_id, is_admin=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, group_id, is_admin) VALUES (?, ?, ?)",
        (user_id, group_id, is_admin),
    )
    conn.commit()
    conn.close()

def is_admin(user_id, group_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE user_id = ? AND group_id = ?", (user_id, group_id))
    result = cursor.fetchone()
    conn.close()
    return result["is_admin"] if result else False

def add_group(group_id, owner_id, group_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO groups (group_id, owner_id, group_name) VALUES (?, ?, ?)",
        (group_id, owner_id, group_name),
    )
    conn.commit()
    conn.close()

def get_group_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT group_id FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result["group_id"] if result else None

def get_menu_text(group_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT menu_text, button_single, button_event FROM groups WHERE group_id = ?", (group_id,)
    )
    result = cursor.fetchone()
    conn.close()
    return result if result else ("Kein Text gesetzt", "Einzeltermin", "Event")