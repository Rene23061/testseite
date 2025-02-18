import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
)
from config import BOT_TOKEN
from admin_panel import admin_menu, list_bookings, list_events, cancel_booking, cancel_event, blacklist_user
from single_booking_bot import register_single_booking_handlers
from gangbang_bot import register_gangbang_booking_handlers

# Logging aktivieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Datenbankverbindung herstellen
def connect_db():
    return sqlite3.connect("/root/eventbot/eventbot.db")

# Menü-Text aus der Datenbank abrufen
def get_menu_text(group_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT menu_text, button_single, button_event FROM groups WHERE group_id = ?", (group_id,))
    result = cursor.fetchone()
    conn.close()
    return result if result else ("Willkommen! Wähle eine Option:", "📅 Einzelbuchung", "🎉 Event buchen")

# Start-Menü anzeigen
async def termin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    group_id = update.message.chat.id
    menu_text, button_single, button_event = get_menu_text(group_id)

    keyboard = [
        [InlineKeyboardButton(button_single, callback_data="single")],
        [InlineKeyboardButton(button_event, callback_data="gangbang")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(menu_text, reply_markup=reply_markup)

# Callback für die Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "single":
        await context.bot.send_message(query.message.chat_id, "Du hast Einzelbuchung gewählt.")
    elif query.data == "gangbang":
        await context.bot.send_message(query.message.chat_id, "Du hast Eventbuchung gewählt.")

# Hauptfunktion zum Starten des Bots
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # CommandHandler registrieren
    app.add_handler(CommandHandler("termin", termin))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Admin-Funktionen
    app.add_handler(CommandHandler("admin", admin_menu))
    app.add_handler(CommandHandler("list_bookings", list_bookings))
    app.add_handler(CommandHandler("list_events", list_events))
    app.add_handler(CommandHandler("cancel_booking", cancel_booking))
    app.add_handler(CommandHandler("cancel_event", cancel_event))
    app.add_handler(CommandHandler("blacklist_user", blacklist_user))

    # Spezifische Buchungs-Handler registrieren
    register_single_booking_handlers(app)
    register_gangbang_booking_handlers(app)

    # Bot starten
    app.run_polling()

if __name__ == "__main__":
    main()