import sqlite3

DB_PATH = "/root/eventbot/eventbot.db"

def initialize_database():
    """ Erstellt die notwendigen Tabellen in der Datenbank, falls sie nicht existieren. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabelle für Gruppen
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER UNIQUE NOT NULL,
            owner_id INTEGER NOT NULL,
            group_name TEXT NOT NULL,
            auto_booking BOOLEAN DEFAULT 0
        )
    """)

    # Tabelle für Nutzer
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            group_id INTEGER NOT NULL,
            is_admin BOOLEAN DEFAULT 0,
            FOREIGN KEY (group_id) REFERENCES groups(group_id)
        )
    """)

    conn.commit()
    conn.close()

def add_group(group_id, owner_id, group_name):
    """ Fügt eine neue Gruppe hinzu, falls sie nicht bereits existiert. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO groups (group_id, owner_id, group_name) VALUES (?, ?, ?)",
                   (group_id, owner_id, group_name))

    conn.commit()
    conn.close()

def add_user(user_id, group_id, is_admin=False):
    """ Fügt einen neuen Benutzer hinzu, falls er nicht existiert. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("INSERT OR IGNORE INTO users (user_id, group_id, is_admin) VALUES (?, ?, ?)",
                   (user_id, group_id, int(is_admin)))

    conn.commit()
    conn.close()

def is_admin(user_id):
    """ Prüft, ob der Nutzer Admin ist. """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT is_admin FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else False