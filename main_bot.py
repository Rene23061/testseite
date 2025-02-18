from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import logging
from database import add_user, get_menu_text
from config import BOT_TOKEN

# Logging einrichten
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Start-Befehl in der Gruppe
async def start_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    bot_username = context.bot.username  # Holt den Bot-Benutzernamen automatisch

    # Erzeugt einen individuellen Start-Link für den privaten Chat
    private_chat_link = f"https://t.me/{bot_username}?start=private"

    # Nachricht mit Link zum Privat-Chat
    text = (
        "📩 Klicke auf den Link, um einen Termin zu buchen: \n"
        f"[➡️ Termin buchen]({private_chat_link})"
    )

    await update.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=True)

# Start-Befehl im privaten Chat
async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Nutzer zur Datenbank hinzufügen
    add_user(user_id, chat_id)

    # Begrüßungstext und Menü aus der Datenbank holen
    menu_text, _, _ = get_menu_text(chat_id)

    await update.message.reply_text(menu_text)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Handler für den Gruppenstart
    application.add_handler(CommandHandler("termin", start_group))

    # Handler für den privaten Start
    application.add_handler(CommandHandler("start", start_private))

    logger.info("🤖 Bot läuft...")
    application.run_polling()

if __name__ == "__main__":
    main()