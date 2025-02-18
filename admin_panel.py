from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from database import is_admin, set_menu_text, get_menu_text

# Admin-Panel anzeigen
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Prüfen, ob der Nutzer ein Admin ist
    if not is_admin(user_id):
        await update.message.reply_text("🚫 Zugriff verweigert. Du bist kein Admin!")
        return
    
    # Aktuelle Menütexte abrufen
    menu_text, button_single, button_event = get_menu_text(chat_id)

    keyboard = [
        [InlineKeyboardButton("📝 Begrüßungstext ändern", callback_data="change_text")],
        [InlineKeyboardButton("📅 Einzelbuchung-Button ändern", callback_data="change_single")],
        [InlineKeyboardButton("🎉 Eventbuchung-Button ändern", callback_data="change_event")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"⚙️ <b>Admin-Panel</b>\n\n"
        f"📜 Begrüßungstext: <i>{menu_text}</i>\n"
        f"📅 Einzelbuchung: <i>{button_single}</i>\n"
        f"🎉 Eventbuchung: <i>{button_event}</i>\n\n"
        "Wähle eine Option, um Änderungen vorzunehmen:",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

# Callback-Handler für Admin-Änderungen
async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = query.message.chat_id

    if not is_admin(user_id):
        await query.answer("🚫 Zugriff verweigert.", show_alert=True)
        return

    # Nachricht aktualisieren und Eingabeaufforderung senden
    if query.data == "change_text":
        context.user_data["admin_action"] = "text"
        await query.message.edit_text("📝 Sende mir den neuen Begrüßungstext:")
    elif query.data == "change_single":
        context.user_data["admin_action"] = "single"
        await query.message.edit_text("📅 Sende mir den neuen Text für den Einzelbuchung-Button:")
    elif query.data == "change_event":
        context.user_data["admin_action"] = "event"
        await query.message.edit_text("🎉 Sende mir den neuen Text für den Eventbuchung-Button:")

# Admin-Nachrichten verarbeiten
async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    if not is_admin(user_id):
        await update.message.reply_text("🚫 Zugriff verweigert.")
        return

    action = context.user_data.get("admin_action")
    if not action:
        await update.message.reply_text("⚠️ Keine aktive Änderung erkannt.")
        return

    new_text = update.message.text
    menu_text, button_single, button_event = get_menu_text(chat_id)

    # Text entsprechend der Admin-Interaktion speichern
    if action == "text":
        menu_text = new_text
    elif action == "single":
        button_single = new_text
    elif action == "event":
        button_event = new_text

    set_menu_text(chat_id, menu_text, button_single, button_event)

    await update.message.reply_text("✅ Änderungen gespeichert!")
    context.user_data["admin_action"] = None  # Reset der Aktion

# Admin-Befehle registrieren
def register_admin_handlers(application):
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CallbackQueryHandler(handle_admin_callback, pattern="^change_"))
    application.add_handler(CommandHandler("text", handle_admin_text))