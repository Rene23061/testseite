import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, is_admin, add_group, get_group_id
from config import BOT_TOKEN

# Logging einrichten
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def starttermin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Nur Admins können den Bot in einer Gruppe starten und registrieren."""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Prüfen, ob der Nutzer Admin ist
    chat_admins = await context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in chat_admins]

    if user_id not in admin_ids:
        await update.message.reply_text(f"@{update.effective_user.username} ❌ Du bist kein Admin und kannst diesen Befehl nicht nutzen!")
        return

    # Gruppe registrieren und Admin speichern
    add_group(chat_id, user_id, update.effective_chat.title)
    add_user(user_id, chat_id, is_admin=True)

    await update.message.reply_text("✅ Diese Gruppe wurde erfolgreich registriert und du wurdest als Admin eingetragen!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Erkennt automatisch, ob es sich um einen Admin oder Nutzer handelt und zeigt das passende Menü."""
    user_id = update.effective_user.id

    # Prüfen, aus welcher Gruppe der Nutzer kommt
    group_id = get_group_id(user_id)
    if not group_id:
        await update.message.reply_text("⚠️ Du bist nicht mit einer registrierten Gruppe verknüpft. Bitte nutze den Bot über eine Gruppe!")
        return

    if is_admin(user_id):
        # Admin-Panel anzeigen
        tastatur = [[InlineKeyboardButton("📌 Einstellungen", callback_data="admin_settings")]]
        reply_markup = InlineKeyboardMarkup(tastatur)
        await update.message.reply_text("🔧 Admin-Panel:", reply_markup=reply_markup)
    else:
        # Nutzer-Menü anzeigen
        tastatur = [
            [InlineKeyboardButton("📅 Einzel-Termin", callback_data="booking_single")],
            [InlineKeyboardButton("🎉 Event-Termin", callback_data="booking_event")]
        ]
        reply_markup = InlineKeyboardMarkup(tastatur)
        await update.message.reply_text("Willkommen! Bitte wähle eine Option:", reply_markup=reply_markup)

def main():
    """Startet den Bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("starttermin", starttermin))
    application.add_handler(CommandHandler("start", start))

    logger.info("Bot erfolgreich gestartet.")
    application.run_polling()

if __name__ == "__main__":
    main()