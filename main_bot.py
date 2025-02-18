import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from database import get_menu_text, add_user, is_admin
from config import BOT_TOKEN

# Logging aktivieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def termin(update: Update, context: CallbackContext):
    """ Befehl /termin verarbeitet: Wechselt in den Privatchat und zeigt das Menü an. """
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    group_id = chat_id  # Falls in einer Gruppe ausgeführt

    # Falls der Befehl in einer Gruppe kommt, Nutzer in Privatchat schicken
    if chat_id < 0:  
        await update.message.reply_text("📩 Bitte schreibe mir privat, um einen Termin zu buchen!")
        return
    
    # Nutzer zur Datenbank hinzufügen
    add_user(user_id, chat_id)

    # Begrüßungstext, Bild & Buttons aus DB holen
    menu_text, menu_image, button_single, button_event = get_menu_text(chat_id)

    # Inline-Buttons erstellen
    keyboard = [
        [InlineKeyboardButton(button_single, callback_data="single")],
        [InlineKeyboardButton(button_event, callback_data="event")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Menü anzeigen (mit Bild falls vorhanden)
    if menu_image:
        await context.bot.send_photo(chat_id=user_id, photo=menu_image, caption=menu_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text(menu_text, reply_markup=reply_markup)

async def button_click(update: Update, context: CallbackContext):
    """ Verarbeitet Klicks auf die Inline-Buttons. """
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "single":
        await query.message.edit_text("📅 Einzelbuchung gewählt. Weiterleitung folgt...")
    elif query.data == "event":
        await query.message.edit_text("🎉 Event-Buchung gewählt. Weiterleitung folgt...")

    # Nachricht nach der Auswahl löschen
    await context.bot.delete_message(chat_id=user_id, message_id=query.message.message_id)

def main():
    """ Startet den Bot mit allen Befehlen. """
    app = Application.builder().token(BOT_TOKEN).build()

    # Befehle registrieren
    app.add_handler(CommandHandler("termin", termin))

    # Callback-Handler für Buttons
    app.add_handler(CallbackQueryHandler(button_click))

    # Bot starten
    logger.info("🤖 Bot läuft...")
    app.run_polling()

if __name__ == "__main__":
    main()