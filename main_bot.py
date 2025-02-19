import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from database import add_user, is_admin, get_group_id
from config import BOT_TOKEN

# Logging aktivieren
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: CallbackContext) -> None:
    """ Startbefehl für Nutzer im privaten Chat. """
    user_id = update.effective_user.id
    group_id = get_group_id(user_id)

    if group_id is None:
        await update.message.reply_text("⚠️ Du bist nicht mit einer registrierten Gruppe verknüpft. Bitte nutze den Bot über eine Gruppe!")
        return

    if is_admin(user_id, group_id):
        await update.message.reply_text("✅ Willkommen Admin! Hier ist dein Admin-Panel.")
    else:
        await update.message.reply_text("👋 Willkommen! Hier sind deine verfügbaren Optionen.")

async def starttermin(update: Update, context: CallbackContext) -> None:
    """ Wird in einer Gruppe aufgerufen, um die Gruppe zu registrieren. """
    chat = update.effective_chat
    user = update.effective_user
    user_id = user.id
    group_id = chat.id

    if not is_admin(user_id, group_id):
        await update.message.reply_text(f"🚫 @{user.username}, du bist kein Admin! Nur Admins können diesen Befehl ausführen.")
        return

    add_user(user_id, group_id, is_admin=True)
    await update.message.reply_text("✅ Gruppe erfolgreich registriert und Admin eingetragen.")

def main() -> None:
    """ Startet den Telegram-Bot. """
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("starttermin", starttermin))

    logging.info("🚀 Bot gestartet...")
    app.run_polling()

if __name__ == "__main__":
    main()