import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from database import add_user, is_admin, get_group_id
from config import BOT_TOKEN

# Logging aktivieren (Debug-Modus)
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG  # DEBUG zeigt alle Meldungen an
)

async def start(update: Update, context: CallbackContext) -> None:
    """ Startbefehl für Nutzer im privaten Chat mit Debugging. """
    user_id = update.effective_user.id
    group_id = get_group_id(user_id)

    logging.debug(f"[PRIVATE CHAT] User-ID: {user_id}, Erkannte Gruppe: {group_id}")

    if group_id is None:
        await update.message.reply_text("⚠️ Du bist nicht mit einer registrierten Gruppe verknüpft. Bitte nutze den Bot über eine Gruppe!")
        return

    admin_status = is_admin(user_id, group_id)
    logging.debug(f"[PRIVATE CHAT] Admin-Status von {user_id} in {group_id}: {admin_status}")

    if admin_status:
        await update.message.reply_text("✅ Willkommen Admin! Hier ist dein Admin-Panel.")
    else:
        await update.message.reply_text("👋 Willkommen! Hier sind deine verfügbaren Optionen.")

async def starttermin(update: Update, context: CallbackContext) -> None:
    """ Wird in einer Gruppe aufgerufen, um die Gruppe zu registrieren. """
    chat = update.effective_chat
    user = update.effective_user
    user_id = user.id
    group_id = chat.id

    logging.debug(f"[GRUPPE] Starttermin-Befehl von User-ID: {user_id} in Gruppe-ID: {group_id}")

    if not is_admin(user_id, group_id):
        logging.warning(f"[GRUPPE] Kein Admin: @{user.username} (User-ID: {user_id}) wollte /starttermin ausführen!")
        await update.message.reply_text(f"🚫 @{user.username}, du bist kein Admin! Nur Admins können diesen Befehl ausführen.")
        return

    try:
        add_user(user_id, group_id, is_admin=True)
        logging.info(f"[Datenbank] Admin {user_id} erfolgreich in Gruppe {group_id} eingetragen.")
        await update.message.reply_text("✅ Gruppe erfolgreich registriert und Admin eingetragen.")
    except Exception as e:
        logging.error(f"[Datenbank] Fehler beim Eintragen in DB: {e}")
        await update.message.reply_text("❌ Fehler beim Eintragen in die Datenbank!")

def main() -> None:
    """ Startet den Telegram-Bot. """
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("starttermin", starttermin))

    logging.info("🚀 Bot gestartet...")
    app.run_polling()

if __name__ == "__main__":
    main()