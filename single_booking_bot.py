from telegram import Update
from telegram.ext import ContextTypes
from database import connect_db

async def book_single(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Funktion für Einzelbuchungen."""
    user_id = update.message.from_user.id
    group_id = update.message.chat.id

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO bookings (user_id, group_id, date_time, status) VALUES (?, ?, datetime('now'), 'Offen')",
                   (user_id, group_id))
    conn.commit()
    cursor.close()
    conn.close()

    await update.message.reply_text("✅ Einzelbuchung wurde erfolgreich registriert!")