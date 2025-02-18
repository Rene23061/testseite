from telegram import Update
from telegram.ext import ContextTypes
from database import connect_db

async def book_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funktion für Party/Event Buchungen."""
    user_id = update.message.from_user.id
    group_id = update.message.chat.id

    conn = connect_db()
    cursor = conn.cursor()

    # Prüfen, ob das Event existiert
    cursor.execute("SELECT id FROM events WHERE group_id = ? AND status = 'Geplant' ORDER BY date_time ASC LIMIT 1", (group_id,))
    event = cursor.fetchone()

    if event:
        event_id = event[0]
        cursor.execute("INSERT INTO event_bookings (user_id, event_id, status) VALUES (?, ?, 'Bestätigt')",
                       (user_id, event_id))
        conn.commit()
        cursor.close()
        conn.close()
        await update.message.reply_text("🎉 Deine Teilnahme am Event wurde bestätigt!")
    else:
        await update.message.reply_text("⚠️ Es gibt aktuell keine geplanten Events für diese Gruppe.")