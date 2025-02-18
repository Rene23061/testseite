import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext
from src.single_booking_bot import register_single_booking_handlers
from src.database import init_db, get_menu_text
from src.config import BOT_TOKEN

# Logging aktivieren
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# SQLite-Datenbank initialisieren
init_db()
print("✅ SQLite-Datenbank ist bereit!")

# /termin Befehl
async def termin(update: Update, context: CallbackContext) -> None:
    group_id = update.effective_chat.id

    # Menü-Texte aus der DB holen
    menu_text, button_single, button_event = get_menu_text(group_id)
    
    keyboard = [
        [InlineKeyboardButton(button_single, callback_data="single")],
        [InlineKeyboardButton(button_event, callback_data="event")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(menu_text, reply_markup=reply_markup)

# Button-Klicks verarbeiten
async def button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    
    if query.data == "single":
        await query.message.reply_text("🔹 Einzeltermin buchen...")
    elif query.data == "event":
        await query.message.reply_text("🎉 Gangbang-Event buchen...")

# Hauptfunktion
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Handler registrieren
    app.add_handler(CommandHandler("termin", termin))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Einzelbuchung-Handlers registrieren
    register_single_booking_handlers(app)

    print("✅ Bot ist online!")
    app.run_polling()

if __name__ == "__main__":
    main()