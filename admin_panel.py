from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler, MessageHandler, filters
from database import set_menu_text, get_menu_text, is_admin

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Zeigt das Admin-Panel zur Bearbeitung des Begrüßungstextes und der Button-Namen. """
    user_id = update.effective_user.id
    group_id = update.effective_chat.id

    if not is_admin(user_id):
        await update.message.reply_text("🚫 Du hast keine Admin-Rechte!")
        return

    menu_text, button_single, button_event = get_menu_text(group_id)

    keyboard = [
        [InlineKeyboardButton("✏ Begrüßungstext ändern", callback_data="edit_text")],
        [InlineKeyboardButton("✏ Einzelbuchungs-Button ändern", callback_data="edit_single")],
        [InlineKeyboardButton("✏ Eventbuchungs-Button ändern", callback_data="edit_event")],
        [InlineKeyboardButton("❌ Admin-Panel schließen", callback_data="close_admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"⚙ <b>Admin-Panel</b>\n\n"
        f"📢 <b>Begrüßungstext:</b> {menu_text}\n"
        f"📅 <b>Einzelbuchung-Button:</b> {button_single}\n"
        f"🎉 <b>Eventbuchung-Button:</b> {button_event}",
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Fordert den Admin auf, einen neuen Begrüßungstext einzugeben. """
    query = update.callback_query
    await query.answer()
    context.user_data["edit_mode"] = "menu_text"
    await query.message.reply_text("✍ Bitte sende den neuen Begrüßungstext.")

async def edit_single(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Fordert den Admin auf, einen neuen Text für den Einzelbuchungs-Button einzugeben. """
    query = update.callback_query
    await query.answer()
    context.user_data["edit_mode"] = "button_single"
    await query.message.reply_text("✍ Bitte sende den neuen Text für den Einzelbuchungs-Button.")

async def edit_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Fordert den Admin auf, einen neuen Text für den Eventbuchungs-Button einzugeben. """
    query = update.callback_query
    await query.answer()
    context.user_data["edit_mode"] = "button_event"
    await query.message.reply_text("✍ Bitte sende den neuen Text für den Eventbuchungs-Button.")

async def save_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Speichert den vom Admin eingegebenen Text in der Datenbank. """
    user_id = update.effective_user.id
    group_id = update.effective_chat.id

    if not is_admin(user_id):
        await update.message.reply_text("🚫 Du hast keine Admin-Rechte!")
        return

    edit_mode = context.user_data.get("edit_mode")
    new_text = update.message.text

    if not edit_mode:
        await update.message.reply_text("⚠️ Keine aktive Änderung erkannt.")
        return

    menu_text, button_single, button_event = get_menu_text(group_id)

    if edit_mode == "menu_text":
        menu_text = new_text
    elif edit_mode == "button_single":
        button_single = new_text
    elif edit_mode == "button_event":
        button_event = new_text

    set_menu_text(group_id, menu_text, button_single, button_event)
    await update.message.reply_text("✅ Änderungen gespeichert!")

    del context.user_data["edit_mode"]

async def close_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ Schließt das Admin-Panel. """
    query = update.callback_query
    await query.answer()
    await query.message.delete()

def register_admin_handlers(application):
    """ Registriert die Admin-Befehle und Callback-Handler. """
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(CallbackQueryHandler(edit_text, pattern="edit_text"))
    application.add_handler(CallbackQueryHandler(edit_single, pattern="edit_single"))
    application.add_handler(CallbackQueryHandler(edit_event, pattern="edit_event"))
    application.add_handler(CallbackQueryHandler(close_admin, pattern="close_admin"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_text))