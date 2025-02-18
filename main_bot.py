from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackContext

BOT_USERNAME = "GbEvent_bot"  # Dein Bot-Username

async def termin(update: Update, context: CallbackContext) -> None:
    """Sendet das Buchungsmenü in die Gruppe."""
    
    keyboard = [
        [InlineKeyboardButton("📅 Einzelbuchung", url=f"https://t.me/{BOT_USERNAME}?start=single")],
        [InlineKeyboardButton("🎉 Event buchen", url=f"https://t.me/{BOT_USERNAME}?start=event")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📩 Wähle deine gewünschte Buchungsart aus:\n"
        "➡ Klicke auf einen Button, um deine Buchung zu starten.",
        reply_markup=reply_markup
    )

async def start(update: Update, context: CallbackContext) -> None:
    """Reagiert auf den Start-Befehl im privaten Chat."""
    
    query = context.args[0] if context.args else None
    
    if query == "single":
        text = "📅 Du hast die Einzelbuchung gewählt! Wähle nun Datum & Uhrzeit."
    elif query == "event":
        text = "🎉 Du hast die Event-Buchung gewählt! Wähle dein Event."
    else:
        text = "👋 Willkommen! Bitte kehre zur Gruppe zurück und starte eine Buchung."

    keyboard = [[InlineKeyboardButton("🔙 Zurück zur Gruppe", url="https://t.me/YOUR_GROUP_LINK")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=reply_markup)

def main():
    """Startet den Bot."""
    application = Application.builder().token("DEIN_BOT_TOKEN").build()

    application.add_handler(CommandHandler("termin", termin))
    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == "__main__":
    main()