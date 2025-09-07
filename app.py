import logging
import pyodbc
import datetime
import io
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import os
from dotenv import load_dotenv
import bot_helpers
import db_helpers


load_dotenv()

# ---------------- CONFIG ----------------
TELEGRAM_TOKEN = os.getenv("BOT_API_KEY")

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize subscribers set
subscribers = set()

# ---------------- GRAPH ----------------
def make_plot(df):
    # Add implementation here
    pass

# ---------------- BOT HANDLERS ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Use /enroll to receive daily reports.")

async def enroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribers.add(chat_id)
    await update.message.reply_text("You have been enrolled for daily reports ✅")

# New handler for all non-command messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all incoming messages that are not commands."""
    message_text = update.message.text
    user_name = update.message.from_user.first_name
    logger.info(f"Received message from {user_name}: {message_text}")

    print(update)
    print(f"Chat ID: {update.message.chat_id} Message text: {message_text}")
    
    # Simple response logic
    response = f"Hello {user_name}! I received your message: '{message_text}'\n\n"
    response += "I can help you with soil moisture data. Use these commands:\n"
    response += "- /start - Get started with the bot\n"
    response += "- /enroll - Receive daily reports"
    
    await update.message.reply_text(response)

# ---------------- DAILY JOB ----------------
async def send_daily_reports(app: Application):
    if not subscribers:
        return
    try:
        for chat_id in subscribers:
            await app.bot.send_message(chat_id=chat_id, text="Here is your daily soil moisture report!")
    except Exception as e:
        logger.error(f"Error sending reports: {e}")

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("enroll", enroll))
    
    # Add handler for regular messages (non-commands)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
