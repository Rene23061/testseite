import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
from database import add_user, is_admin, get_group_id, add_group

# Logging einrichten
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Start-Funktion, erkennt Gruppe und Nutzerrolle """
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Prüfen, ob der Nutzer über den Link gekommen ist (/start?group=123456)
    args = context.args
    group_id = None
    if args:
        try:
            group_id = int(args[0].replace("group=", ""))
        except ValueError:
            pass

    # Falls keine Gruppe übergeben wurde, die zuletzt bekannte Gruppe aus der Datenbank holen
    if not group_id:
        group_id = get_group_id(user_id)

    if not group_id:
        await update.message.reply_text("❌ Fehler: Ich konnte keine Gruppe zuordnen!")
        return

    # Nutzer zur Datenbank hinzufügen (falls noch nicht vorhanden)
    add_user(user_id, group_id)

    # Prüfen, ob der Nutzer Admin ist
    if is_admin(user_id):
        await show_admin_panel(update, context)
    else:
        await show_booking_menu(update, context)

async def starttermin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Nur Admins können diesen Befehl ausführen, um eine Gruppe zu registrieren """
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Prüfen, ob der Nutzer Admin in dieser Gruppe ist
    member = await context.bot.get_chat_member(chat_id, user_id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text(f"❌ @{update.effective_user.username}, du bist kein Admin!")
        return

    # Gruppe zur Datenbank hinzufügen
    group_name = update.effective_chat.title
    add_group(chat_id, user_id, group_name)

    await update.message.reply_text(f"✅ Die Gruppe '{group_name}' wurde erfolgreich registriert!")

async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Admin-Panel anzeigen """
    keyboard = [
        [InlineKeyboardButton("🔧 Einstellungen", callback_data="admin_settings")],
        [InlineKeyboardButton("📅 Termine verwalten", callback_data="admin_appointments")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("👑 Willkommen im Admin-Panel!", reply_markup=reply_markup)

async def show_booking_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Normales Buchungsmenü anzeigen """
    keyboard = [
        [InlineKeyboardButton("🔹 Einzel buchen", callback_data="single_booking")],
        [InlineKeyboardButton("🔸 Event buchen", callback_data="event_booking")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("🔥 Wähle deine Buchung:", reply_markup=reply_markup)

def main():
    """ Startet den Bot """
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("starttermin", starttermin))
    application.add_handler(CallbackQueryHandler(show_admin_panel, pattern="^admin_"))
    application.add_handler(CallbackQueryHandler(show_booking_menu, pattern="^single_booking|event_booking"))

    logger.info("Bot erfolgreich gestartet!")
    application.run_polling()

if __name__ == "__main__":
    main()