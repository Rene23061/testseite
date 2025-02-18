import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, is_admin, get_group_id
from config import BOT_TOKEN

# Logging einrichten
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Start-Funktion
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Prüfen, ob der Start-Befehl eine Gruppen-ID enthält
    if context.args:
        group_id = context.args[0].replace("group_", "")
    else:
        group_id = get_group_id(user_id)

    if not group_id:
        await update.message.reply_text("⚠ Du wurdest keiner Gruppe zugeordnet.")
        return

    # Nutzer in der Datenbank speichern, falls nicht vorhanden
    add_user(user_id, group_id)

    # Prüfen, ob der Nutzer ein Admin ist
    if is_admin(user_id):
        await show_admin_panel(update, context)
    else:
        await show_user_menu(update, context, group_id)

# Admin-Panel anzeigen
async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🔧 Einstellungen", callback_data="admin_settings")],
        [InlineKeyboardButton("📅 Termine verwalten", callback_data="admin_appointments")],
        [InlineKeyboardButton("❌ Schließen", callback_data="close")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🔹 **Admin-Panel** 🔹\n\nWähle eine Option:", reply_markup=reply_markup)

# Nutzer-Menü anzeigen
async def show_user_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, group_id: str) -> None:
    keyboard = [
        [InlineKeyboardButton("📅 Einzeltermin", callback_data=f"book_single_{group_id}")],
        [InlineKeyboardButton("👥 Event-Termin", callback_data=f"book_event_{group_id}")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🔹 **Willkommen!** 🔹\n\nWähle eine Buchungsoption:", reply_markup=reply_markup)

# Hauptfunktion
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_admin_panel, pattern="^admin_.*"))

    logger.info("Bot gestartet...")
    application.run_polling()

if __name__ == "__main__":
    main()