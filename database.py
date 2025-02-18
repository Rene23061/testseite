import sqlite3

DB_PATH = "eventbot.db"

def connect_db():
    """ Erstellt eine Verbindung zur SQLite-Datenbank. """
    return sqlite3.connect(DB_PATH)

def create_tables():
    """ Erstellt alle benötigten Tabellen, falls sie nicht existieren. """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER UNIQUE NOT NULL,
            owner_id INTEGER NOT NULL,
            group_name TEXT NOT NULL,
            auto_booking BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            group_id INTEGER,
            phone_number TEXT,
            total_bookings INTEGER DEFAULT 0,
            total_cancellations INTEGER DEFAULT 0,
            vip_status BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );

        CREATE TABLE IF NOT EXISTS providers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            telegram_id INTEGER NOT NULL,
            group_id INTEGER,
            pricing TEXT,
            availability TEXT,
            custom_texts TEXT,
            booking_mode TEXT CHECK (booking_mode IN ('einzeln', 'event', 'beides')),
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            provider_id INTEGER,
            group_id INTEGER,
            date_time TEXT NOT NULL,
            status TEXT CHECK (status IN ('Bestätigt', 'Offen', 'Abgesagt')),
            payment_status TEXT CHECK (payment_status IN ('Bezahlt', 'Offen')),
            extras_selected TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (provider_id) REFERENCES providers(id),
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            provider_id INTEGER,
            group_id INTEGER,
            date_time TEXT NOT NULL,
            max_participants INTEGER NOT NULL,
            price_per_person REAL,
            location TEXT,
            location_notes TEXT,
            status TEXT CHECK (status IN ('Geplant', 'Voll', 'Abgesagt')),
            FOREIGN KEY (provider_id) REFERENCES providers(id),
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );

        CREATE TABLE IF NOT EXISTS event_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_id INTEGER,
            status TEXT CHECK (status IN ('Bestätigt', 'Storniert')),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (event_id) REFERENCES events(id)
        );

        CREATE TABLE IF NOT EXISTS blacklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date_added TEXT DEFAULT CURRENT_TIMESTAMP,
            reason TEXT,
            total_strikes INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            provider_id INTEGER,
            group_id INTEGER,
            amount REAL,
            payment_method TEXT CHECK (payment_method IN ('PayPal', 'Krypto', 'Barzahlung')),
            payment_date TEXT DEFAULT CURRENT_TIMESTAMP,
            refund_status TEXT CHECK (refund_status IN ('Erstattet', 'Nicht erstattet')),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (provider_id) REFERENCES providers(id),
            FOREIGN KEY (group_id) REFERENCES groups(id)
        );

        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            reminder_time TEXT NOT NULL,
            reminder_text TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    conn.commit()
    conn.close()

def add_user(telegram_id, group_id):
    """ Fügt einen neuen Benutzer hinzu, wenn er noch nicht existiert. """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, group_id, total_bookings, total_cancellations, vip_status) 
        VALUES (?, ?, 0, 0, FALSE)
        ON CONFLICT(telegram_id) DO NOTHING;
    """, (telegram_id, group_id))
    conn.commit()
    conn.close()

def get_upcoming_reminders():
    """ Holt Erinnerungen für bevorstehende Termine. """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.telegram_id, reminders.reminder_text
        FROM reminders
        JOIN users ON reminders.user_id = users.id
        WHERE reminders.reminder_time <= datetime('now', '+24 hours')
    """)
    
    reminders = cursor.fetchall()
    conn.close()
    return reminders

if __name__ == "__main__":
    create_tables()
    print("✅ SQLite-Datenbank ist bereit!")