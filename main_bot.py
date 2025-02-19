import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from database import add_user, is_admin, get_group_id, add_group
from config import BOT_TOKEN

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Begrüßt den Nutzer und zeigt je nach Status das richtige Menü an."""
    user_id = update.message.from_user.id
    args = context.args

    if args:
        group_id = args[0]  # Falls die Gruppen-ID mitgegeben wurde
        logging.info(f"DEBUG: Erkannte group_id durch Start-Link: {group_id}")
    else:
        group_id = get_group_id(user_id)  # Falls keine mitgegeben wurde, aus DB holen

    if not group_id:
        await update.message.reply_text("⚠️ Du bist nicht mit einer registrierten Gruppe verknüpft.")
        return

    if is_admin(user_id, group_id):
        await update.message.reply_text("🔧 Admin-Panel geöffnet!")
        show_admin_panel(update, context)
    else:
        await update.message.reply_text("📅 Willkommensnachricht + Buttons!")
        show_user_menu(update, context)

async def starttermin(update: Update, context: CallbackContext) -> None:
    """Fügt die Gruppe und den Admin zur Datenbank hinzu."""
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    group_name = update.message.chat.title

    if not is_admin(user_id, chat_id):
        await update.message.reply_text(f"⚠️ {update.message.from_user.username}, du bist kein Admin!")
        return

    add_group(chat_id, user_id, group_name)
    add_user(user_id, chat_id, True)

    await update.message.reply_text("✅ Gruppe und Admin erfolgreich registriert!")

def show_admin_panel(update: Update, context: CallbackContext):
    """Zeigt das Admin-Panel an."""
    update.message.reply_text("🔧 Admin-Panel: Hier kannst du deine Einstellungen verwalten.")

def show_user_menu(update: Update, context: CallbackContext):
    """Zeigt das Benutzer-Menü an."""
    update.message.reply_text("📅 Dein Benutzer-Menü mit Optionen.")

def main():
    """Startet den Bot."""
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("starttermin", starttermin))

    application.run_polling()

if __name__ == "__main__":
    main()