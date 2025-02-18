from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

def start_gangbang_booking(update: Update, context: CallbackContext):
    """ Zeigt die Eventbuchungsauswahl an. """
    keyboard = [
        [InlineKeyboardButton("Bestätigen", callback_data="confirm_event")],
        [InlineKeyboardButton("Abbrechen", callback_data="cancel_event")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Du hast eine Event-Buchung gewählt. Bestätige bitte:",
        reply_markup=reply_markup
    )

def handle_gangbang_booking(update: Update, context: CallbackContext):
    """ Reagiert auf die Auswahl. """
    query = update.callback_query
    query.answer()

    if query.data == "confirm_event":
        query.edit_message_text("✅ Event-Buchung bestätigt!")
    elif query.data == "cancel_event":
        query.edit_message_text("❌ Event-Buchung abgebrochen.")