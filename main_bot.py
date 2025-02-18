import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import add_user, get_menu_text, is_admin
from config import BOT_TOKEN  # Token wird aus config.py geladen

# Logging einrichten
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot-Startbefehl
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Prüfen, ob der Nutzer über einen Gruppenlink kommt
    if update.message and update.message.text.startswith("/start"):
        args = context.args
        group_id = None
        if args:
            group_id = args[0]  # Gruppen-ID aus der URL übernehmen

        # Nutzer zur Datenbank hinzufügen
        add_user(user_id, group_id)

        # Prüfen, ob der Nutzer Admin ist
        admin_status = is_admin(user_id)

        if admin_status:
            await show_admin_menu(update, context)
            return

        # Menü-Text, Button-Namen und Bild abrufen
        menu_text, button_single, button_event, image_url = get_menu_text(group_id)

        keyboard = [
            [InlineKeyboardButton(button_single, callback_data="single_booking")],
            [InlineKeyboardButton(button_event, callback_data="event_booking")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Bild senden, falls vorhanden
        if image_url and image_url != "none":
            try:
                await context.bot.send_photo(chat_id=user_id, photo=image_url, caption=menu_text, reply_markup=reply_markup)
            except Exception as e:
                logger.error(f"Fehler beim Senden des Bildes: {e}")
                await context.bot.send_message(chat_id=user_id, text=menu_text, reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=user_id, text=menu_text, reply_markup=reply_markup)

# Callback für Admin-Panel
async def show_admin_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Texte & Bilder bearbeiten", callback_data="edit_content")],
        [InlineKeyboardButton("Termine verwalten", callback_data="manage_bookings")],
        [InlineKeyboardButton("Schließen", callback_data="close_admin")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("📌 **Admin-Panel**", reply_markup=reply_markup)

# Callback für Auswahl Einzel- oder Eventbuchung
async def booking_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "single_booking":
        await query.edit_message_text("🔹 Einzelbuchung wurde gewählt. Weitere Details folgen...")
    elif query.data == "event_booking":
        await query.edit_message_text("🎉 Eventbuchung wurde gewählt. Weitere Details folgen...")

# Hauptfunktion zum Starten des Bots
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(booking_selection, pattern="^(single_booking|event_booking)$"))

    logger.info("🤖 Bot gestartet...")
    application.run_polling()

if __name__ == "__main__":
    main()