from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from transformers import pipeline
import random

# የቦት ቶከን (ከ@BotFather ያገኙትን ያስገቡ)
TOKEN = "YOUR_BOT_TOKEN_HERE"

# NLP ሞዴል መጀመር (የጽሑፍ ማመንጨት)
nlp = pipeline("text-generation", model="distilgpt2")

# ቀልዶች ዝርዝር
jokes = [
    "ለምን ዶሮ መንገድ ተሻገረች? 🐔 ሌላኛው ጎን ለመድረስ! 😄",
    "ቲማቲም ለምን ቀይ ሆነ? ምክንያቱም ብዙ ተሸማቀቀ! 🍅",
    "ብዕር ለምን ዘፈነ? ምክንያቱም ተንቀጠቀጠ! ✍️"
]

# የ/start ትዕዛዝ
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"ሰላም {user_name}! እኔ Umer AI ነኝ፣ እንደ ሰው የምነጋገር ቦት። 😊\n"
        "ምንም ጻፍልኝ፣ ቀልድ ንገረኝ (/joke)፣ ወይም /help ተጠቀም ምን ማድረግ እንደምችል ለማወቅ!"
    )

# የ/help ትዕዛዝ
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(
        f"{user_name}፣ እኔ Umer AI ነኝ! ምን ማድረግ እችላለሁ? 🤖\n"
        "- /start: መግቢያ መልእክት\n"
        "- /help: ይህን መልእክት ያሳያል\n"
        "- /joke: ቀልድ ይነግራል\n"
        "- ማንኛውንም ጥያቄ ጻፍ፣ እንደ ጓደኛ እመልሳለሁ!"
    )

# የ/joke ትዕዛዝ
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.from_user.first_name
    random_joke = random.choice(jokes)
    await update.message.reply_text(
        f"{user_name}፣ ይህን ቀልድ እንዴት አየህ? 😄\n{random_joke}\nሌላ ቀልድ ትፈልጋለህ?"
    )

# የመልእክት አያያዝ ተግባር
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    user_name = update.message.from_user.first_name

    # ቀላል ሰላምታ መልሶች
    if "ሰላም" in user_message:
        response = f"ሰላም {user_name}! ዛሬ ጥሩ ነው እንዴ? 😊 ምን ልንወያይ?"
    elif "እንደምን" in user_message or "ምን እየሰራህ" in user_message:
        response = f"{user_name}፣ እኔ Umer AI ነኝ፣ እዚህ ከአንተ ጋር እየተወያየሁ ነው! 😎 አንተ ምን እየሰራህ ነው?"
    elif "ቀልድ" in user_message:
        random_joke = random.choice(jokes)
        response = f"{user_name}፣ እንደዚህ ያለ ቀልድስ? 😄\n{random_joke}"
    else:
        # NLP ሞዴል በመጠቀም መልስ ማመንጨት
        try:
            nlp_response = nlp(f"ተጠቃሚው ሲል: {user_message}. እንደ Umer AI መልስ:", max_length=50, num_return_sequences=1)[0]['generated_text']
            response = f"{user_name}፣ {nlp_response.split(':')[-1].strip()} 😊 ሌላ ምን እንወያይ?"
        except Exception as e:
            response = f"{user_name}፣ ይቅርታ ሙሉ በሙሉ አልገባኝም፣ ነገር ግን እንደ ጓደኛ ልመልስህ እሞክራለሁ! 😄 ሌላ ምን አለ?"

    await update.message.reply_text(response)

# የስህተት አያያዝ
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"ስህተት ተከስቷል: {context.error}")
    if update:
        await update.message.reply_text("ይቅርታ፣ አንድ ነገር ተሳስቷል። እንደገና ሞክር!")

def main():
    # የቦት መተግበሪያ መፍጠር
    app = Application.builder().token(TOKEN).build()

    # ትዕዛዞችን እና መልእክቶችን መቆጣጠሪያ መጨመር
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error)

    # ቦቱን ማስጀመር
    print("Umer AI ቦት ጀምሯል...")
    app.run_polling()

if __name__ == "__main__":
    main()
