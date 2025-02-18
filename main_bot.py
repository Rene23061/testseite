from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, is_admin, get_group_id, add_group
from config import BOT_TOKEN
import logging

# Logging einrichten
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Start-Funktion mit Gruppen-Check
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id

    # Gruppen-ID aus dem Start-Link holen
    args = context.args
    if args:
        group_id = args[0]  # Gruppen-ID aus dem Link
        add_user(user_id, group_id, is_admin=is_admin(user_id))  # Nutzer speichern
    else:
        group_id = get_group_id(user_id)  # Falls keine Gruppen-ID mitgegeben wurde

    if not group_id:
        await update.message.reply_text("⚠️ Du bist nicht mit einer registrierten Gruppe verknüpft. Bitte nutze den Bot über eine Gruppe!")
        return

    if is_admin(user_id):
        # Admin-Panel anzeigen
        tastatur = [
            [InlineKeyboardButton("📌 Einstellungen", callback_data="admin_settings")],
            [InlineKeyboardButton("📅 Termine verwalten", callback_data="admin_appointments")],
            [InlineKeyboardButton("🚪 Schließen", callback_data="admin_close")]
        ]
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

# Startbefehl für Gruppen-Admins (nur 1x pro Gruppe)
async def starttermin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    user_id = update.effective_user.id

    # Prüfen, ob der Nutzer Admin der Gruppe ist
    member = await context.bot.get_chat_member(chat.id, user_id)
    if member.status not in ["administrator", "creator"]:
        await update.message.reply_text(f"⚠️ @${update.effective_user.username}, du bist kein Admin und darfst diesen Befehl nicht nutzen!")
        return

    # Gruppe und Admin eintragen
    add_group(chat.id, user_id, chat.title)
    await update.message.reply_text("✅ Diese Gruppe wurde erfolgreich registriert!")

# Handler-Funktion für Callback-Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "booking_single":
        await query.message.reply_text("📅 Du hast Einzel-Termin gewählt. Wir kontaktieren dich bald.")
    elif query.data == "booking_event":
        await query.message.reply_text("🎉 Du hast Event-Termin gewählt. Wir kontaktieren dich bald.")
    elif query.data == "admin_settings":
        await query.message.reply_text("⚙️ Hier kannst du die Einstellungen ändern.")
    elif query.data == "admin_appointments":
        await query.message.reply_text("📅 Hier kannst du Termine verwalten.")
    elif query.data == "admin_close":
        await query.message.reply_text("🔒 Admin-Panel geschlossen.")

# Hauptfunktion zum Starten des Bots
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("starttermin", starttermin))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot gestartet...")
    application.run_polling()

if __name__ == "__main__":
    main()