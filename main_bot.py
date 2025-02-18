from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import logging
from database import add_user, get_menu_data
from config import BOT_TOKEN
import requests  # Zum Überprüfen der Bild-URL

# Logging einrichten
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Standardwerte, falls nichts in der Datenbank hinterlegt ist
DEFAULT_IMAGE = "https://yourserver.com/no_image.jpg"
DEFAULT_TEXT = "Willkommen! Bitte wähle eine Option:"

# Funktion zur Überprüfung, ob die Bild-URL gültig ist
def is_valid_image(url):
    try:
        response = requests.head(url, timeout=5)
        content_type = response.headers.get("Content-Type", "")
        return response.status_code == 200 and "image" in content_type
    except Exception:
        return False

# Start im privaten Chat (nach Klick auf den Link)
async def start_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    # Nutzer zur Datenbank hinzufügen
    add_user(user_id, chat_id)

    # Menü-Daten aus der Datenbank abrufen (Text, Bild, Button-Namen)
    menu_text, menu_image, button_single, button_event = get_menu_data(chat_id)

    # Falls kein Text oder Bild gespeichert wurde → Standardwert setzen
    if not menu_text:
        menu_text = DEFAULT_TEXT
    if not menu_image or not is_valid_image(menu_image):
        menu_image = DEFAULT_IMAGE  # Falls ungültig, Standardbild verwenden

    # Inline-Buttons erstellen
    keyboard = [
        [InlineKeyboardButton(button_single, callback_data="single_booking")],
        [InlineKeyboardButton(button_event, callback_data="event_booking")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Begrüßungsnachricht mit Bild senden
    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=menu_image,
            caption=menu_text,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Fehler beim Senden des Bildes: {e}")
        await context.bot.send_message(chat_id=chat_id, text=menu_text, reply_markup=reply_markup)

# Auswahl im Menü (Einzel oder Event)
async def menu_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id

    # Nutzer hat Einzel- oder Eventbuchung gewählt
    if query.data == "single_booking":
        await query.message.edit_caption("📅 Einzelbuchung ausgewählt! Weitere Schritte folgen…")
    elif query.data == "event_booking":
        await query.message.edit_caption("🎉 Eventbuchung ausgewählt! Weitere Schritte folgen…")

# Hauptfunktion
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Handler für den Start im privaten Chat
    application.add_handler(CommandHandler("start", start_private))

    # Handler für die Menü-Auswahl
    application.add_handler(CallbackQueryHandler(menu_selection, pattern="^(single_booking|event_booking)$"))

    logger.info("🤖 Bot läuft...")
    application.run_polling()

if __name__ == "__main__":
    main()