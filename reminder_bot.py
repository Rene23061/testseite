import time
from telegram import Bot
from database import get_upcoming_reminders
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)

def send_reminders():
    """ Sendet Erinnerungen an Kunden für bevorstehende Buchungen. """
    reminders = get_upcoming_reminders()

    for reminder in reminders:
        user_id, reminder_text = reminder
        try:
            bot.send_message(chat_id=user_id, text=f"🔔 Erinnerung: {reminder_text}")
            print(f"✅ Erinnerung gesendet an {user_id}")
        except Exception as e:
            print(f"❌ Fehler beim Senden an {user_id}: {e}")

while True:
    send_reminders()
    time.sleep(600)  # Alle 10 Minuten prüfen