import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import update_group_settings, get_group_settings

# Logging einrichten
logger = logging.getLogger(__name__)

async def admin_panel(update: Update, context: CallbackContext) -> None:
    """ Zeigt das Admin-Panel mit den Optionen an. """
    keyboard = [
        [InlineKeyboardButton("✏️ Begrüßungstext ändern", callback_data="edit_welcome_text")],
        [InlineKeyboardButton("🖋 Button-Namen ändern", callback_data="edit_button_names")],
        [InlineKeyboardButton("📅 Termine verwalten", callback_data="manage_appointments")],
        [InlineKeyboardButton("❌ Schließen", callback_data="close_admin_panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.message.edit_text("⚙️ Admin-Panel:\n\nWähle eine Option:", reply_markup=reply_markup)

async def edit_welcome_text(update: Update, context: CallbackContext) -> None:
    """ Admin kann den Begrüßungstext für die Gruppe ändern. """
    await update.callback_query.message.reply_text("✏️ Sende mir den neuen Begrüßungstext.")
    context.user_data['awaiting_text'] = True

async def edit_button_names(update: Update, context: CallbackContext) -> None:
    """ Admin kann die Namen der Buttons ändern. """
    await update.callback_query.message.reply_text("✏️ Sende mir die neuen Button-Namen im Format:\n\n`Einzel | Event`")
    context.user_data['awaiting_buttons'] = True

async def manage_appointments(update: Update, context: CallbackContext) -> None:
    """ Öffnet das Terminverwaltungsmenü. """
    await update.callback_query.message.reply_text("📅 Terminverwaltung folgt noch...")

async def close_admin_panel(update: Update, context: CallbackContext) -> None:
    """ Schließt das Admin-Panel. """
    await update.callback_query.message.edit_text("Admin-Panel geschlossen.")

async def handle_text(update: Update, context: CallbackContext) -> None:
    """ Verarbeitet eingegebenen Begrüßungstext oder Button-Namen. """
    user_id = update.effective_user.id
    group_id = get_group_settings(user_id)

    if 'awaiting_text' in context.user_data and context.user_data['awaiting_text']:
        new_text = update.message.text
        update_group_settings(group_id, "menu_text", new_text)
        await update.message.reply_text("✅ Begrüßungstext wurde aktualisiert.")
        context.user_data['awaiting_text'] = False

    elif 'awaiting_buttons' in context.user_data and context.user_data['awaiting_buttons']:
        button_names = update.message.text.split(" | ")
        if len(button_names) == 2:
            update_group_settings(group_id, "button_single", button_names[0])
            update_group_settings(group_id, "button_event", button_names[1])
            await update.message.reply_text("✅ Button-Namen wurden aktualisiert.")
        else:
            await update.message.reply_text("⚠️ Bitte sende die Namen im korrekten Format: `Einzel | Event`")
        context.user_data['awaiting_buttons'] = False

def register_admin_handlers(application):
    """ Registriert alle Admin-bezogenen Callback-Handler. """
    application.add_handler(CallbackQueryHandler(admin_panel, pattern="^admin_panel$"))
    application.add_handler(CallbackQueryHandler(edit_welcome_text, pattern="^edit_welcome_text$"))
    application.add_handler(CallbackQueryHandler(edit_button_names, pattern="^edit_button_names$"))
    application.add_handler(CallbackQueryHandler(manage_appointments, pattern="^manage_appointments$"))
    application.add_handler(CallbackQueryHandler(close_admin_panel, pattern="^close_admin_panel$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))