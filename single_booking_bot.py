from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext

def start_single_booking(update: Update, context: CallbackContext):
    """ Zeigt die Einzelbuchungsauswahl an. """
    keyboard = [
        [InlineKeyboardButton("Bestätigen", callback_data="confirm_single")],
        [InlineKeyboardButton("Abbrechen", callback_data="cancel_single")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Du hast eine Einzelbuchung gewählt. Bestätige bitte:",
        reply_markup=reply_markup
    )

def handle_single_booking(update: Update, context: CallbackContext):
    """ Reagiert auf die Auswahl. """
    query = update.callback_query
    query.answer()

    if query.data == "confirm_single":
        query.edit_message_text("✅ Einzelbuchung bestätigt!")
    elif query.data == "cancel_single":
        query.edit_message_text("❌ Einzelbuchung abgebrochen.")