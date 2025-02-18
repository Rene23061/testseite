import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
DB_PATH = "eventbot.db"

def connect_db():
    """ Erstellt eine Verbindung zur SQLite-Datenbank. """
    return sqlite3.connect(DB_PATH)

def create_tables():
    """ Erstellt die notwendigen Tabellen, falls sie noch nicht existieren. """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS groups (
        group_id INTEGER PRIMARY KEY,
        menu_text TEXT DEFAULT 'Willkommen! Wähle eine Option:',
        button_single TEXT DEFAULT '📅 Einzeltermin buchen',
        button_event TEXT DEFAULT '🎉 Event buchen'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE NOT NULL,
        group_id INTEGER,
        is_admin BOOLEAN DEFAULT FALSE
    )
    """)

    conn.commit()
    conn.close()

def is_admin(user_id):
    """ Prüft, ob der Nutzer ein Admin ist. """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT is_admin FROM users WHERE telegram_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result[0]

def set_menu_text(group_id, menu_text, button_single, button_event):
    """ Setzt den Begrüßungstext und die Button-Namen für eine Gruppe. """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO groups (group_id, menu_text, button_single, button_event)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(group_id) DO UPDATE 
        SET menu_text = ?, button_single = ?, button_event = ?
    """, (group_id, menu_text, button_single, button_event, menu_text, button_single, button_event))
    conn.commit()
    conn.close()

def get_menu_text(group_id):
    """ Ruft den Begrüßungstext und die Button-Namen für eine Gruppe ab. """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT menu_text, button_single, button_event FROM groups WHERE group_id = ?", (group_id,))
    result = cursor.fetchone()
    conn.close()
    return result if result else ("Willkommen! Wähle eine Option:", "📅 Einzeltermin buchen", "🎉 Event buchen")

def add_user(telegram_id, group_id, is_admin=False):
    """ Fügt einen neuen Benutzer hinzu oder aktualisiert den Admin-Status. """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, group_id, is_admin)
        VALUES (?, ?, ?)
        ON CONFLICT(telegram_id) DO UPDATE 
        SET group_id = ?, is_admin = ?
    """, (telegram_id, group_id, is_admin, group_id, is_admin))
    conn.commit()
    conn.close()