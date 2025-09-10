import logging
import datetime
import io
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
from dotenv import load_dotenv
import bot_helpers
import db_helpers
import pytz

load_dotenv()

# ---------------- CONFIG ----------------
TELEGRAM_TOKEN = os.getenv("BOT_API_KEY")

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------- BOT HANDLERS ----------------
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if not context.args:
        return await update.effective_chat.send_message("Incorrect password. Access denied ❌")

    if bot_helpers.check_password(context.args[0]):
        if db_helpers.is_subscriber(chat_id):
            return await update.effective_chat.send_message("You are already subscribed to daily reports ✅")
        else:
            db_helpers.add_subscriber(chat_id)
            return await update.effective_chat.send_message("You have subscribed to daily reports ✅")
    else:
        return await update.effective_chat.send_message("Incorrect password. Access denied ❌")
    
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if db_helpers.is_subscriber(chat_id):
        if db_helpers.remove_subscriber(chat_id):
            return await update.effective_chat.send_message("You have unsubscribed from daily reports ✅")
        else:
            return await update.effective_chat.send_message("An error occurred while trying to unsubscribe, please try again later ❌")
    else:
        return await update.effective_chat.send_message("You are not currently subscribed ❌")

# ---------------- DAILY JOB ----------------
async def send_daily_reports(context: ContextTypes.DEFAULT_TYPE):
    subscribers = db_helpers.get_subscribers()

    for row in subscribers:
        try:
            await context.bot.send_photo(chat_id=str(row[0]), photo=bot_helpers.generate_moisture_plot(), caption=bot_helpers.message_builder())
        except Exception as e:
            logger.error(f"Error sending reports: {e}")

async def send_daily_reports_manual(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subscribers = db_helpers.get_subscribers()

    for row in subscribers:
        try:
            await context.bot.send_photo(chat_id=str(row[0]), photo=bot_helpers.generate_moisture_plot(), caption=bot_helpers.message_builder())
        except Exception as e:
            logger.error(f"Error sending reports: {e}")

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("unsubscribe", unsubscribe))
    app.add_handler(CommandHandler("manual", send_daily_reports_manual))

    # Schedule daily reports at 9 AM
    timezone = pytz.timezone("Europe/Stockholm")
    app.job_queue.run_daily(send_daily_reports, time=datetime.time(hour=22, minute=20, second=0, tzinfo=timezone))

    app.run_polling()

if __name__ == "__main__":
    main()
