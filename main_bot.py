import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, get_menu_text

# Logging konfigurieren
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Start-Befehl für den Bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Nutzer in der Datenbank hinzufügen
    add_user(user_id, chat_id)

    # Menü-Text und Buttons aus der Datenbank abrufen
    menu_text, button_single, button_event = get_menu_text(chat_id)

    # Inline-Buttons erstellen
    keyboard = [
        [InlineKeyboardButton(button_single, callback_data='single')],
        [InlineKeyboardButton(button_event, callback_data='event')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Nachricht mit den Auswahl-Buttons senden
    await update.message.reply_text(menu_text, reply_markup=reply_markup)

# Callback-Handler für die Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if query.data == 'single':
        await context.bot.send_message(chat_id=user_id, text="Du hast eine Einzelbuchung ausgewählt.")
    elif query.data == 'event':
        await context.bot.send_message(chat_id=user_id, text="Du hast eine Eventbuchung ausgewählt.")

    await query.answer()

def main():
    # Bot-Token aus der config.py laden
    from config import BOT_TOKEN

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("termin", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot läuft...")
    application.run_polling()

if __name__ == "__main__":
    main()