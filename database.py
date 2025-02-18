import sqlite3

# Datenbankverbindung herstellen
def connect_db():
    return sqlite3.connect("eventbot.db")

# Tabelle erstellen (falls sie nicht existiert)
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL,
        group_id INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS menu_texts (
        group_id INTEGER PRIMARY KEY,
        menu_text TEXT DEFAULT 'Willkommen! Wähle deine Option:',
        button_single TEXT DEFAULT '📅 Einzelbuchung',
        button_event TEXT DEFAULT '🎉 Eventbuchung'
    );
    """)

    conn.commit()
    conn.close()

# Benutzer zur Datenbank hinzufügen
def add_user(telegram_id, group_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (telegram_id, group_id)
    VALUES (?, ?)
    ON CONFLICT(telegram_id) DO NOTHING;
    """, (telegram_id, group_id))

    conn.commit()
    conn.close()

# Überprüfen, ob ein Nutzer Admin ist
def is_admin(telegram_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM admins WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()

    conn.close()
    return result is not None

# Menütext und Buttons abrufen
def get_menu_text(group_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT menu_text, button_single, button_event FROM menu_texts WHERE group_id = ?
    """, (group_id,))
    result = cursor.fetchone()

    conn.close()
    
    if result:
        return result
    return "Willkommen! Wähle eine Option:", "📅 Einzelbuchung", "🎉 Eventbuchung"

# Menütexte in der Datenbank setzen
def set_menu_text(group_id, menu_text, button_single, button_event):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO menu_texts (group_id, menu_text, button_single, button_event)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(group_id) 
    DO UPDATE SET menu_text = excluded.menu_text, 
                  button_single = excluded.button_single, 
                  button_event = excluded.button_event;
    """, (group_id, menu_text, button_single, button_event))

    conn.commit()
    conn.close()

# Initialisiere die Datenbank beim Start
init_db()