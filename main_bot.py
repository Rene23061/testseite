from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
from database import add_user, get_menu_text, is_admin
from config import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Nutzer zur Datenbank hinzufügen
    add_user(user_id, chat_id)

    # Menütext und Buttons aus der Datenbank holen
    menu_text, button_single, button_event = get_menu_text(chat_id)

    # Inline-Buttons erstellen
    keyboard = [
        [InlineKeyboardButton(button_single, callback_data='single')],
        [InlineKeyboardButton(button_event, callback_data='event')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(menu_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == 'single':
        await query.edit_message_text("Einzelbuchung: Bitte schreibe mir privat!")
    elif query.data == 'event':
        await query.edit_message_text("Eventbuchung: Bitte schreibe mir privat!")

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("termin", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot läuft...")
    application.run_polling()

if __name__ == "__main__":
    main()