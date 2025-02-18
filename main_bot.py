from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import logging
from database import add_user, get_menu_text
from config import BOT_TOKEN

# Logging einrichten
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    username = update.effective_user.username

    # Nutzer zur Datenbank hinzufügen
    add_user(user_id, chat_id)

    # Menütext und Buttons aus der Datenbank holen
    menu_text, button_single, button_event = get_menu_text(chat_id)

    # Link zum privaten Chat mit dem Bot
    bot_username = context.bot.username
    private_chat_link = f"https://t.me/{bot_username}?start=private"

    # Inline-Buttons erstellen
    keyboard = [
        [InlineKeyboardButton(button_single, url=private_chat_link)],
        [InlineKeyboardButton(button_event, url=private_chat_link)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(menu_text, reply_markup=reply_markup)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("termin", start))

    logger.info("🤖 Bot läuft...")
    application.run_polling()

if __name__ == "__main__":
    main()