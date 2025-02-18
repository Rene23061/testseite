import sqlite3

DB_PATH = "/root/eventbot/eventbot.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

def add_user(telegram_id, group_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (telegram_id, group_id, total_bookings, total_cancellations, vip_status) 
        VALUES (?, ?, 0, 0, FALSE) 
        ON CONFLICT(telegram_id, group_id) DO NOTHING;
    """, (telegram_id, group_id))
    conn.commit()
    cursor.close()
    conn.close()