import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext

# Logging aktivieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Verbindung zur SQLite-Datenbank herstellen
DB_PATH = "eventbot.db"  # Pfad zur SQLite-Datenbank

def connect_db():
    """Verbindet sich mit der SQLite-Datenbank."""
    return sqlite3.connect(DB_PATH)

# Admin-Check Funktion
async def is_admin(update: Update, context: CallbackContext) -> bool:
    """Prüft, ob der Benutzer ein Admin in der Gruppe ist."""
    user_id = update.effective_user.id
    chat_id = update.message.chat.id

    try:
        chat_admins = await context.bot.get_chat_administrators(chat_id)
        return any(admin.user.id == user_id for admin in chat_admins)
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Admins: {e}")
        return False

# Begrüßungsnachricht mit Inline-Buttons
async def start(update: Update, context: CallbackContext) -> None:
    """Reagiert auf /start und leitet Nutzer ins Menü."""
    user_id = update.effective_user.id
    chat_id = update.message.chat.id

    if await is_admin(update, context):  # Prüft, ob der User ein Admin ist
        await update.message.reply_text("👑 Willkommen im Admin-Panel!\nWähle eine Option:", reply_markup=admin_menu())
    else:
        await update.message.reply_text("📩 Bitte schreibe mir privat, um einen Termin zu buchen.", reply_markup=user_menu())

# Admin-Panel Buttons
def admin_menu():
    """Erstellt die Inline-Tastatur für das Admin-Panel."""
    keyboard = [
        [InlineKeyboardButton("📜 Texte & Bilder", callback_data="admin_texts")],
        [InlineKeyboardButton("📅 Termine verwalten", callback_data="admin_appointments")],
        [InlineKeyboardButton("🔄 Schließen", callback_data="admin_close")]
    ]
    return InlineKeyboardMarkup(keyboard)

# User-Menü Buttons
def user_menu():
    """Erstellt die Inline-Tastatur für normale Benutzer."""
    keyboard = [
        [InlineKeyboardButton("📆 Einzeltermin buchen", callback_data="book_single")],
        [InlineKeyboardButton("🎉 Event buchen", callback_data="book_event")]
    ]
    return InlineKeyboardMarkup(keyboard)

# Callback-Handler für Admin-Buttons
async def admin_callback(update: Update, context: CallbackContext) -> None:
    """Verarbeitet die Auswahl im Admin-Panel."""
    query = update.callback_query
    await query.answer()

    if query.data == "admin_texts":
        await query.edit_message_text("📜 Hier kannst du Begrüßungstext & Bild ändern.")
    elif query.data == "admin_appointments":
        await query.edit_message_text("📅 Hier kannst du Termine verwalten.")
    elif query.data == "admin_close":
        await query.edit_message_text("🔄 Admin-Panel geschlossen.")

# Callback-Handler für User-Buttons
async def user_callback(update: Update, context: CallbackContext) -> None:
    """Verarbeitet die Auswahl im Benutzer-Menü."""
    query = update.callback_query
    await query.answer()

    if query.data == "book_single":
        await query.edit_message_text("📆 Einzeltermin gebucht! 🎉")
    elif query.data == "book_event":
        await query.edit_message_text("🎉 Eventbuchung bestätigt! 🎟")

# Hauptfunktion zum Starten des Bots
def main():
    """Startet den Bot."""
    application = Application.builder().token("DEIN_BOT_TOKEN").build()

    # Befehle hinzufügen
    application.add_handler(CommandHandler("start", start))

    # Callback-Handler für Inline-Buttons
    application.add_handler(CallbackQueryHandler(admin_callback, pattern="admin_.*"))
    application.add_handler(CallbackQueryHandler(user_callback, pattern="book_.*"))

    logger.info("🤖 Bot läuft...")
    application.run_polling()

if __name__ == "__main__":
    main()