import logging
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Replace with your tokens
TELEGRAM_BOT_TOKEN = "8107798260:AAEkpepBlixiU2KmMh6mLCl9HVtzqaXTM8s"
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
