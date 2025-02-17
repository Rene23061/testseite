from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CallbackQueryHandler
from src.database import add_event_booking

async def start_gangbang_booking(update: Update, context: CallbackContext):
    """Startet die Eventbuchung."""
    keyboard = [
        [InlineKeyboardButton("🎟 Teilnahme bestätigen", callback_data="join_event")],
        [InlineKeyboardButton("❌ Absagen", callback_data="cancel_event")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.reply_text(
        "🔥 Möchtest du am nächsten Gangbang-Event teilnehmen?",
        reply_markup=reply_markup
    )

async def process_event_booking(update: Update, context: CallbackContext):
    """Speichert die Eventbuchung."""
    query = update.callback_query
    user_id = update.effective_user.id
    event_id = 1  # Später dynamisch aus der Datenbank holen

    if query.data == "join_event":
        add_event_booking(user_id, event_id, "Bestätigt")
        await query.message.reply_text("✅ Du bist für das Event angemeldet!")
    elif query.data == "cancel_event":
        add_event_booking(user_id, event_id, "Storniert")
        await query.message.reply_text("❌ Deine Teilnahme wurde storniert.")

def register_handlers(application):
    """Registriert die Callback-Handler für Gangbang-Events."""
    application.add_handler(CallbackQueryHandler(start_gangbang_booking, pattern="^gangbang$"))
    application.add_handler(CallbackQueryHandler(process_event_booking, pattern="^(join_event|cancel_event)$"))
