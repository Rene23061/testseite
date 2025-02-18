from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN
from database import initialize_database, add_group, add_user, is_admin
import logging

# Logging einrichten
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Datenbank initialisieren
initialize_database()

# Funktion zum Starten der Gruppenregistrierung (nur für Admins)
async def start_termin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    user = update.effective_user

    if chat.type != "supergroup" and chat.type != "group":
        await update.message.reply_text("Dieser Befehl kann nur in Gruppen ausgeführt werden!")
        return

    add_group(chat.id, user.id, chat.title)
    await update.message.reply_text(f"✅ Die Gruppe **{chat.title}** wurde erfolgreich registriert!")

# Funktion, die auf den Start-Link reagiert
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    chat_id = update.effective_chat.id
    user_id = user.id

    # Überprüfen, ob der Nutzer Admin ist
    admin_status = is_admin(user_id)

    # Nutzer registrieren
    add_user(user_id, chat_id, is_admin=admin_status)

    if admin_status:
        await admin_panel(update, context)
    else:
        await show_booking_options(update, context)

# Funktion zum Anzeigen des Admin-Panels
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("📄 Begrüßungstext ändern", callback_data="admin_edit_text")],
        [InlineKeyboardButton("🔘 Button-Namen ändern", callback_data="admin_edit_buttons")],
        [InlineKeyboardButton("❌ Admin-Panel schließen", callback_data="admin_close")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔧 **Admin-Panel**\nWähle eine Option:", reply_markup=reply_markup)

# Funktion zum Anzeigen der Buchungsoptionen für Nutzer
async def show_booking_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("👤 Einzel-Termin", callback_data="booking_single")],
        [InlineKeyboardButton("👥 Event-Termin", callback_data="booking_event")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Willkommen! Wähle eine Option:", reply_markup=reply_markup)

# Hauptfunktion zum Starten des Bots
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Handler für Befehle
    application.add_handler(CommandHandler("starttermin", start_termin))
    application.add_handler(CommandHandler("start", start))

    # Callback-Handler für Admin-Panel und Buchung
    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_.*"))
    application.add_handler(CallbackQueryHandler(show_booking_options, pattern="^booking_.*"))

    # Bot starten
    logger.info("Bot erfolgreich gestartet und läuft jetzt...")
    application.run_polling()

if __name__ == "__main__":
    main()