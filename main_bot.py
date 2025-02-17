from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from src.config import BOT_TOKEN
from src.single_booking_bot import register_handlers as register_single_booking_handlers
from src.gangbang_bot import register_handlers as register_gangbang_handlers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Begrüßt den Nutzer und zeigt das Hauptmenü."""
    keyboard = [
        [InlineKeyboardButton("📅 Einzeltermin buchen", callback_data="single")],
        [InlineKeyboardButton("🎉 Event buchen (Gangbang)", callback_data="gangbang")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "👋 Willkommen!\n\nWähle aus, was du buchen möchtest:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verarbeitet die Auswahl aus dem Hauptmenü."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "single":
        await query.message.reply_text("📅 Einzeltermin-Buchung wird gestartet...")
    elif query.data == "gangbang":
        await query.message.reply_text("🎉 Event-Buchung wird gestartet...")

def main():
    """Startet den Telegram-Bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("termin", termin))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    # Einzel- und Event-Buchungen registrieren
    register_single_booking_handlers(app)
    register_gangbang_handlers(app)

    print("✅ Bot ist online!")
    app.run_polling()

if __name__ == "__main__":
    main()