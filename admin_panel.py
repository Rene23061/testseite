from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from database import update_admin_settings, get_admin_settings

def open_admin_panel(update: Update, context: CallbackContext):
    """ Zeigt das Admin-Panel mit Optionen an. """
    user_id = update.message.chat_id
    settings = get_admin_settings(user_id)

    if not settings:
        update.message.reply_text("❌ Du hast keine Admin-Berechtigung!")
        return

    keyboard = [
        [InlineKeyboardButton("📜 Begrüßungstext ändern", callback_data="edit_text")],
        [InlineKeyboardButton("🖼 Bild ändern", callback_data="edit_image")],
        [InlineKeyboardButton("🔘 Button-Namen ändern", callback_data="edit_buttons")],
        [InlineKeyboardButton("❌ Schließen", callback_data="close_admin")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f"⚙️ Admin-Panel ⚙️\n\n"
        f"📝 Begrüßungstext: {settings['welcome_text']}\n"
        f"🖼 Bild: {settings['image_url']}\n"
        f"🔘 Einzelbuchung: {settings['button_single']}\n"
        f"🔘 Eventbuchung: {settings['button_event']}",
        reply_markup=reply_markup
    )

def handle_admin_action(update: Update, context: CallbackContext):
    """ Behandelt die Auswahl aus dem Admin-Panel. """
    query = update.callback_query
    query.answer()

    if query.data == "edit_text":
        query.edit_message_text("✏️ Sende den neuen Begrüßungstext.")
        context.user_data["admin_edit"] = "text"

    elif query.data == "edit_image":
        query.edit_message_text("📷 Sende den neuen Bild-Link.")
        context.user_data["admin_edit"] = "image"

    elif query.data == "edit_buttons":
        query.edit_message_text("🔘 Sende neue Namen für die Buttons (Einzel,Event) getrennt durch `,`.")
        context.user_data["admin_edit"] = "buttons"

    elif query.data == "close_admin":
        query.edit_message_text("✅ Admin-Panel geschlossen.")

def save_admin_change(update: Update, context: CallbackContext):
    """ Speichert Änderungen der Admin-Einstellungen. """
    user_id = update.message.chat_id
    new_value = update.message.text

    if "admin_edit" not in context.user_data:
        return

    setting_type = context.user_data.pop("admin_edit")

    if setting_type == "text":
        update_admin_settings(user_id, "welcome_text", new_value)
        update.message.reply_text("✅ Begrüßungstext aktualisiert!")

    elif setting_type == "image":
        update_admin_settings(user_id, "image_url", new_value)
        update.message.reply_text("✅ Bild aktualisiert!")

    elif setting_type == "buttons":
        buttons = new_value.split(",")
        if len(buttons) == 2:
            update_admin_settings(user_id, "button_single", buttons[0].strip())
            update_admin_settings(user_id, "button_event", buttons[1].strip())
            update.message.reply_text("✅ Buttons aktualisiert!")
        else:
            update.message.reply_text("⚠️ Falsches Format! Nutze: `Einzel,Event`.")