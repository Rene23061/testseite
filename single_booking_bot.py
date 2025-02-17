from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from src.database import add_booking
import datetime

async def start_single_booking(update: Update, context: CallbackContext):
    """Startet die Einzelbuchung."""
    keyboard = [
        [InlineKeyboardButton("30 Min", callback_data="30"),
         InlineKeyboardButton("60 Min", callback_data="60")],
        [InlineKeyboardButton("90 Min", callback_data="90"),
         InlineKeyboardButton("120 Min", callback_data="120")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(
        "⏳ Wähle die gewünschte Dauer:",
        reply_markup=reply_markup
    )

async def process_booking(update: Update, context: CallbackContext):
    """Speichert die Buchung in der Datenbank."""
    query = update.callback_query
    duration = int(query.data)

    user_id = update.effective_user.id
    group_id = update.effective_chat.id
    date_time = datetime.datetime.now() + datetime.timedelta(hours=1)  # Termin in 1 Stunde

    booking_id = add_booking(user_id, None, group_id, date_time, f"{duration} Min")

    await query.answer()
    await query.message.reply_text(f"✅ Termin für {duration} Minuten gebucht!\nBuchungs-ID: {booking_id}")

def register_handlers(application):
    """Registriert die Callback-Handler für den Buchungsprozess."""
    application.add_handler(CallbackQueryHandler(start_single_booking, pattern="single"))
    application.add_handler(CallbackQueryHandler(process_booking, pattern="^[0-9]+$"))
