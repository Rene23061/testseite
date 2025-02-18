import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, is_admin
from config import BOT_TOKEN

# Logging einrichten
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Funktion zum Starten des Bots und zur Erfassung des Users
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_id = user.id

    # Nutzer zur Datenbank hinzufügen
    add_user(user_id, chat_id)

    # Prüfen, ob der Nutzer Admin ist
    admin_status = is_admin(user_id)

    if admin_status:
        await update.message.reply_text(
            "🔧 Willkommen im Admin-Panel!\nHier kannst du Einstellungen vornehmen.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Einstellungen", callback_data="admin_settings")]
            ]),
        )
    else:
        await update.message.reply_text(
            "Willkommen! Bitte wähle eine Option:",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Einzelbuchung", callback_data="booking_single")],
                [InlineKeyboardButton("Eventbuchung", callback_data="booking_event")],
            ]),
        )

# Funktion für den Befehl /starttermin (nur für Admins)
async def starttermin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if not is_admin(user_id):
        await update.message.reply_text("🚫 Du bist kein Admin und kannst diesen Befehl nicht ausführen.")
        return

    await update.message.reply_text(
        "✅ Gruppe wurde registriert! Der Bot ist jetzt aktiv."
    )

# Callback-Funktion für Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "admin_settings":
        await query.message.reply_text("Hier kannst du deine Einstellungen ändern.")
    elif query.data == "booking_single":
        await query.message.reply_text("Du hast eine Einzelbuchung gewählt.")
    elif query.data == "booking_event":
        await query.message.reply_text("Du hast eine Eventbuchung gewählt.")

# Hauptfunktion
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("starttermin", starttermin))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("🤖 Bot gestartet...")
    application.run_polling()

if __name__ == "__main__":
    main()