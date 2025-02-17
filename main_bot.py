
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from src.config import BOT_TOKEN
from src.single_booking_bot import start_single_booking
from src.gangbang_bot import start_gangbang_booking

def start(update: Update, context: CallbackContext):
    """Begrüßt den Nutzer und zeigt das Hauptmenü."""
    keyboard = [
        [InlineKeyboardButton("📅 Einzeltermin buchen", callback_data="single")],
        [InlineKeyboardButton("🎉 Event buchen (Gangbang)", callback_data="gangbang")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "👋 Willkommen!\n\nWähle aus, was du buchen möchtest:",
        reply_markup=reply_markup
    )

def button_handler(update: Update, context: CallbackContext):
    """Verarbeitet die Auswahl aus dem Hauptmenü."""
    query = update.callback_query
    query.answer()
    
    if query.data == "single":
        start_single_booking(update, context)  # Einzeltermin starten
    elif query.data == "gangbang":
        start_gangbang_booking(update, context)  # Event-Buchung starten

def main():
    """Startet den Telegram-Bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()