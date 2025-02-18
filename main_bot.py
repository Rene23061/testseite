import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, is_admin, get_menu_text
from config import BOT_TOKEN

# Logging einrichten
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start-Funktion für den Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Nutzer zur Datenbank hinzufügen
    add_user(user_id, chat_id)

    # Prüfen, ob der Nutzer Admin ist
    admin_status = is_admin(user_id, chat_id)

    # Menü-Text und Buttons aus der Datenbank holen
    menu_text, button_single, button_event = get_menu_text(chat_id)

    # Standardwerte setzen, falls keine Daten vorhanden sind
    if not menu_text:
        menu_text = "Willkommen! Wähle eine Option:"
    if not button_single:
        button_single = "Einzeltermin buchen"
    if not button_event:
        button_event = "Event buchen"

    keyboard = [
        [InlineKeyboardButton(button_single, callback_data="single")],
        [InlineKeyboardButton(button_event, callback_data="event")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Nachricht mit Auswahl senden
    await context.bot.send_message(chat_id=user_id, text=menu_text, reply_markup=reply_markup)

    # Wenn der Nutzer ein Admin ist, Admin-Panel anzeigen
    if admin_status:
        await show_admin_panel(update, context)

# Admin-Panel anzeigen
async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    keyboard = [
        [InlineKeyboardButton("Einstellungen", callback_data="admin_settings")],
        [InlineKeyboardButton("Termine verwalten", callback_data="admin_appointments")],
        [InlineKeyboardButton("Schließen", callback_data="close")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=user_id, text="🔧 Admin-Panel", reply_markup=reply_markup)

# Callback-Handler für Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    query.answer()

    if query.data == "single":
        await query.edit_message_text("Du hast Einzelbuchung gewählt.")
    elif query.data == "event":
        await query.edit_message_text("Du hast Event-Buchung gewählt.")
    elif query.data == "admin_settings":
        await query.edit_message_text("⚙️ Admin-Einstellungen")
    elif query.data == "admin_appointments":
        await query.edit_message_text("📅 Terminverwaltung")
    elif query.data == "close":
        await query.edit_message_text("Admin-Panel geschlossen.")

# Hauptfunktion für den Bot
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler, pattern=".*"))

    logger.info("Bot gestartet...")
    application.run_polling()

if __name__ == "__main__":
    main()