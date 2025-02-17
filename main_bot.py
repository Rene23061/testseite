from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from src.config import BOT_TOKEN
from src.database import get_menu_text

async def termin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Der Befehl /termin schickt den Nutzer in den privaten Chat."""
    user_id = update.effective_user.id
    group_id = update.effective_chat.id  # Gruppen-ID erfassen
    
    menu_text, button_single, button_event = get_menu_text(group_id)

    keyboard = [
        [InlineKeyboardButton(button_single, callback_data="single")],
        [InlineKeyboardButton(button_event, callback_data="gangbang")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Sende dem Nutzer eine private Nachricht mit dem Menü
    await context.bot.send_message(
        chat_id=user_id,
        text=menu_text,
        reply_markup=reply_markup
    )

    # Informiere in der Gruppe, dass der Nutzer eine DM erhalten hat (optional)
    if update.effective_chat.type != "private":
        await update.message.reply_text("📩 Bitte prüfe deine privaten Nachrichten, um einen Termin zu buchen.")

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

    # Befehle registrieren
    app.add_handler(CommandHandler("termin", termin))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot ist online!")
    app.run_polling()

if __name__ == "__main__":
    main()