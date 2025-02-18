import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler
from database import get_menu_text, add_user, is_admin
from config import BOT_TOKEN

# Logging für Fehleranalyse
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def termin(update: Update, context: CallbackContext) -> None:
    """ Wird aufgerufen, wenn ein Nutzer /termin eingibt. Leitet ihn in den Privat-Chat. """
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    group_id = chat_id  # Gruppen-ID ist gleich Chat-ID

    # Nutzer in der Datenbank anlegen, falls noch nicht vorhanden
    add_user(user_id, group_id)

    # Admin-Status prüfen
    admin_status = is_admin(user_id, group_id)

    # Begrüßungstext & Button-Namen aus der Datenbank holen
    menu_text, button_single, button_event, image_path = get_menu_text(group_id)

    # Inline-Buttons erstellen
    buttons = [
        [InlineKeyboardButton(button_single, callback_data="single")],
        [InlineKeyboardButton(button_event, callback_data="event")]
    ]

    if admin_status:
        buttons.append([InlineKeyboardButton("🛠 Admin-Panel", callback_data="admin")])

    reply_markup = InlineKeyboardMarkup(buttons)

    # Nachricht mit Bild senden
    if image_path:
        await context.bot.send_photo(
            chat_id=user_id,
            photo=InputFile(image_path),
            caption=menu_text,
            reply_markup=reply_markup
        )
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text=menu_text,
            reply_markup=reply_markup
        )

async def button_handler(update: Update, context: CallbackContext) -> None:
    """ Behandelt Button-Klicks im Hauptmenü. """
    query = update.callback_query
    query.answer()

    if query.data == "single":
        await query.edit_message_text(text="Du hast Einzelbuchung gewählt.")
    elif query.data == "event":
        await query.edit_message_text(text="Du hast Eventbuchung gewählt.")
    elif query.data == "admin":
        await query.edit_message_text(text="⚙ Willkommen im Admin-Panel!")

def main():
    """ Startet den Bot. """
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("termin", termin))
    app.add_handler(CallbackQueryHandler(button_handler))

    logger.info("✅ Bot ist gestartet!")
    app.run_polling()

if __name__ == "__main__":
    main()