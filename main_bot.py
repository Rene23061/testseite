from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from single_booking_bot import start_single_booking
from gangbang_bot import start_gangbang_booking

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Einzeltermin buchen", callback_data="single")],
        [InlineKeyboardButton("Gangbang-Event buchen", callback_data="gangbang")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(
        "Willkommen! Was möchtest du buchen?",
        reply_markup=reply_markup
    )

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    if query.data == "single":
        start_single_booking(update, context)  # Startet den Einzelbuchungs-Bot
    elif query.data == "gangbang":
        start_gangbang_booking(update, context)  # Startet den Gangbang-Bot

def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN", use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()