from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import get_menu_text
from config import BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Begrüßungstext und Menü anzeigen."""
    group_id = update.effective_chat.id
    menu_text, button_single, button_event = get_menu_text(group_id)

    keyboard = [
        [InlineKeyboardButton(button_single, callback_data="single")],
        [InlineKeyboardButton(button_event, callback_data="event")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(menu_text, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Button-Klicks auswerten."""
    query = update.callback_query
    await query.answer()

    if query.data == "single":
        await query.message.reply_text("➡ Du hast Einzelbuchung gewählt!")
    elif query.data == "event":
        await query.message.reply_text("🎉 Du hast Party/Event gewählt!")

def main():
    """Startet den Telegram-Bot."""
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot ist online!")
    app.run_polling()

if __name__ == "__main__":
    main()