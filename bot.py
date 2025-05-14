import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from telegram.error import TelegramError
import logging

# የlog መደበኛ ቅንብር
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# error handler
async def error_handler(update, context):
    logger.error("Exception while handling an update:", exc_info=context.error)

application.add_error_handler(error_handler)
# Replace with your tokens
TELEGRAM_BOT_TOKEN = "7873450175:AAEs02Wm-fQOX7M4SgdoMVeBmujZXSWssbE"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ሰላም! ምን ልርዳህ?")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )
    reply = response["choices"][0]["message"]["content"]
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.run_polling()

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"ስህተት ተከስቷል: {context.error}")
    if update:
        await update.message.reply_text("ይቅርታ፣ ስህተት ተከስቷል። እባክዎ ቆይተው ይሞክሩ።")

# መቆጣጠሪያውን መጨመር
app.add_error_handler(error_handler)
