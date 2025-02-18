from telegram import Update
from telegram.ext import ContextTypes
from database import connect_db

async def admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin-Panel Hauptmenü."""
    user_id = update.message.from_user.id
    group_id = update.message.chat.id

    conn = connect_db()
    cursor = conn.cursor()

    # Prüfen, ob Nutzer Admin ist
    cursor.execute("SELECT id FROM providers WHERE telegram_id = ? AND group_id = ?", (user_id, group_id))
    admin = cursor.fetchone()

    if admin:
        menu_text = (
            "🔧 *Admin-Panel*\n"
            "1️⃣ /list_bookings – Alle Buchungen anzeigen\n"
            "2️⃣ /list_events – Alle geplanten Events anzeigen\n"
            "3️⃣ /cancel_booking <ID> – Buchung stornieren\n"
            "4️⃣ /cancel_event <ID> – Event absagen\n"
            "5️⃣ /blacklist_user <ID> – Nutzer sperren"
        )
        await update.message.reply_text(menu_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ Du hast keine Admin-Rechte.")

async def list_bookings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Alle Buchungen anzeigen."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, provider_id, date_time, status FROM bookings ORDER BY date_time DESC")
    bookings = cursor.fetchall()
    cursor.close()
    conn.close()

    if bookings:
        response = "📅 *Buchungen:*\n"
        for b in bookings:
            response += f"🔹 ID: {b[0]}, User: {b[1]}, Anbieter: {b[2]}, Datum: {b[3]}, Status: {b[4]}\n"
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        await update.message.reply_text("ℹ️ Keine Buchungen gefunden.")

async def list_events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Alle Events anzeigen."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, provider_id, date_time, max_participants, status FROM events ORDER BY date_time DESC")
    events = cursor.fetchall()
    cursor.close()
    conn.close()

    if events:
        response = "🎉 *Events:*\n"
        for e in events:
            response += f"🔹 ID: {e[0]}, Anbieter: {e[1]}, Datum: {e[2]}, Plätze: {e[3]}, Status: {e[4]}\n"
        await update.message.reply_text(response, parse_mode="Markdown")
    else:
        await update.message.reply_text("ℹ️ Keine geplanten Events gefunden.")

async def cancel_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Buchung stornieren."""
    if not context.args:
        await update.message.reply_text("❌ Bitte eine Buchungs-ID angeben. Beispiel: /cancel_booking 3")
        return

    booking_id = context.args[0]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = 'Storniert' WHERE id = ?", (booking_id,))
    conn.commit()
    cursor.close()
    conn.close()

    await update.message.reply_text(f"✅ Buchung {booking_id} wurde storniert.")

async def cancel_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Event absagen."""
    if not context.args:
        await update.message.reply_text("❌ Bitte eine Event-ID angeben. Beispiel: /cancel_event 2")
        return

    event_id = context.args[0]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE events SET status = 'Abgesagt' WHERE id = ?", (event_id,))
    conn.commit()
    cursor.close()
    conn.close()

    await update.message.reply_text(f"⚠️ Event {event_id} wurde abgesagt.")

async def blacklist_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Nutzer auf die Blacklist setzen."""
    if not context.args:
        await update.message.reply_text("❌ Bitte eine User-ID angeben. Beispiel: /blacklist_user 12345678")
        return

    user_id = context.args[0]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO blacklist (user_id, reason, total_strikes) VALUES (?, 'Admin-Sperre', 1)", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

    await update.message.reply_text(f"🚫 Nutzer {user_id} wurde auf die Blacklist gesetzt.")
