from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import is_admin  # Funktion zur Überprüfung, ob der Benutzer Admin ist

# Funktion zum Anzeigen des Admin-Startmenüs
async def show_admin_panel(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id

    # Überprüfen, ob der Benutzer Admin ist
    if not is_admin(user_id):
        await update.message.reply_text("🚫 Zugriff verweigert: Du bist kein Admin!")
        return

    keyboard = [
        [InlineKeyboardButton("🖊 Begrüßungstext & Bild ändern", callback_data="edit_text_image")],
        [InlineKeyboardButton("📅 Buchungen verwalten", callback_data="manage_bookings")],
        [InlineKeyboardButton("❌ Admin-Panel schließen", callback_data="close_admin")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🔧 **Admin-Panel**\n\nWillkommen im Admin-Bereich. Wähle eine Option:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Funktion zur Bearbeitung von Texten & Bildern
async def edit_text_image(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "🖊 **Texte & Bilder bearbeiten**\n\n"
        "Sende mir den neuen Begrüßungstext oder ein Bild, das im Startmenü angezeigt werden soll.",
        parse_mode="Markdown"
    )

# Funktion zur Verwaltung von Buchungen (Platzhalter für spätere Features)
async def manage_bookings(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "📅 **Buchungen verwalten**\n\n"
        "Hier kannst du alle Buchungen sehen & bearbeiten. Diese Funktion wird bald hinzugefügt.",
        parse_mode="Markdown"
    )

# Funktion zum Schließen des Admin-Panels
async def close_admin(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("✅ Admin-Panel geschlossen.")

# Callback-Handler für das Admin-Menü registrieren
def register_admin_handlers(application):
    application.add_handler(CallbackQueryHandler(edit_text_image, pattern="edit_text_image"))
    application.add_handler(CallbackQueryHandler(manage_bookings, pattern="manage_bookings"))
    application.add_handler(CallbackQueryHandler(close_admin, pattern="close_admin"))