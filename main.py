#### 1. **main.py**
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

LANGUAGE_KEYBOARD = [['Amharic', 'English']]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Choose language / ቋንቋ ይምረጡ:",
        reply_markup=ReplyKeyboardMarkup(LANGUAGE_KEYBOARD, one_time_keyboard=True)
    )

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("እናመሰግናለን! ዘፈኑ ተቀባል።")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thanks! Your music has been received.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "ዝግጅት" in text or "event" in text:
        await update.message.reply_text("የቀረቡ ዝግጅቶች እነዚህ ናቸው:\n1. አዲስ ኮንሰርት\n2. ንግግር ፕሮግራም")
    elif "group" in text or "ቡድን" in text:
        await update.message.reply_text("የቡድኑ ሊንክ: https://t.me/unity_group_et")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VOICE, handle_voice))
app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == '__main__':
    print("Bot running...")
    app.run_polling()
```

---
