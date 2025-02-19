import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from database import add_user, is_admin, add_group, get_group_id
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def starttermin(update: Update, context: CallbackContext) -> None:
    """Nur Admins können die Gruppe registrieren"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Admin-Check
    if not await is_admin(user_id, chat_id, context):
        await update.message.reply_text(f"⚠️ @{update.effective_user.username}, du bist kein Admin und kannst /starttermin nicht nutzen!")
        return
    
    # Gruppe und Admin speichern
    add_group(chat_id, user_id, "Gruppe")
    add_user(user_id, chat_id, True)

    await update.message.reply_text("✅ Gruppe wurde erfolgreich registriert und du bist als Admin eingetragen!")

async def start(update: Update, context: CallbackContext) -> None:
    """Prüft, ob User aus einer registrierten Gruppe kommt"""
    user_id = update.effective_user.id
    group_id = get_group_id(user_id)

    if not group_id:
        await update.message.reply_text("⚠️ Du bist nicht mit einer registrierten Gruppe verknüpft. Bitte nutze den Bot über eine Gruppe!")
        return

    if is_admin(user_id, group_id):
        await update.message.reply_text("📢 Admin-Panel wird geladen...")
        # Hier könnte das Admin-Menü geöffnet werden
    else:
        await update.message.reply_text("📅 Termine werden geladen...")
        # Hier könnten Termine geladen werden

def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("starttermin", starttermin))
    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == "__main__":
    main()