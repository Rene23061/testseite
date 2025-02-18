from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, is_admin, get_menu_text
import logging

# Logging einrichten
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot-Token aus der config-Datei
from config import BOT_TOKEN

# Funktion für den Startbefehl /termin in der Gruppe
async def termin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    first_name = update.effective_user.first_name

    # Prüfen, ob der Nutzer bereits in der Datenbank ist, sonst hinzufügen
    add_user(user_id, chat_id)

    # Begrüßungstext & Button-Namen aus der Datenbank abrufen
    menu_text, button_single, button_event = get_menu_text(chat_id)

    # Inline-Buttons erstellen
    keyboard = [
        [InlineKeyboardButton(button_single, callback_data="single_booking")],
        [InlineKeyboardButton(button_event, callback_data="event_booking")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Nachricht mit Buttons senden
    message = await update.message.reply_text(
        f"{menu_text}\n\n🔽 Wähle eine Option: 🔽",
        reply_markup=reply_markup
    )

    # Nachricht nach Auswahl automatisch löschen
    context.user_data['last_message_id'] = message.message_id

# Funktion zum Verarbeiten der Auswahl (Einzelbuchung/Event)
async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = query.message.chat.id

    # Lösche die Nachricht in der Gruppe
    try:
        await context.bot.delete_message(chat_id, query.message.message_id)
    except Exception as e:
        logger.warning(f"Fehler beim Löschen der Nachricht: {e}")

    # Weiterleitung in den privaten Chat
    if query.data == "single_booking":
        await context.bot.send_message(
            chat_id=user_id,
            text="📅 Einzelbuchung gestartet! Wähle dein Datum und deine Uhrzeit."
        )
    elif query.data == "event_booking":
        await context.bot.send_message(
            chat_id=user_id,
            text="🎉 Eventbuchung gestartet! Wähle dein Event und sichere deinen Platz."
        )

# Hauptfunktion zum Starten des Bots
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Befehl-Handler
    application.add_handler(CommandHandler("termin", termin))
    
    # Auswahl-Handler (Einzelbuchung/Event)
    application.add_handler(CallbackQueryHandler(handle_selection, pattern="^(single_booking|event_booking)$"))

    logger.info("Bot gestartet... 🚀")
    application.run_polling()

if __name__ == "__main__":
    main()