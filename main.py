from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import re

# የቦት ቶከን (ከ@BotFather ያገኙትን ያስገቡ)
TOKEN = "YOUR_BOT_TOKEN_HERE"

# የ/start ትዕዛዝ ተግባር
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ሰላም! እኔ እንደ ሰው የምመልስ ቦት ነኝ። 😊\n"
        "ምን ማድረግ እንደምችል ለማወቅ /help ተጠቀም፣ ወይም ማንኛውንም ጻፍልኝ!"
    )

# የ/help ትዕዛዝ ተግባር
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "እኔ ምን ማድረግ እችላለሁ? 🤖\n"
        "- /start: መግቢያ መልእክት ያሳያል\n"
        "- /help: ይህን መልእክት ያሳያል\n"
        "- /joke: ቀልድ ይነግርሃል\n"
        "- ቀላል ሒሳብ ጻፍ (ለምሳሌ፣ '2 + 2')፣ እፈታለሁ\n"
        "- የአየር ሁኔታ ጠይቅ (ለምሳሌ፣ 'የአዲስ አበባ አየር ሁኔታ')"
    )

# የ/joke ትዕዛዝ ተግባር
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ለምን ዶሮ መንገድ ተሻገረች? 🐔\n"
        "ሌላኛው ጎን ለመድረስ! 😄 ሌላ ቀልድ ትፈልጋለህ?"
    )

# የመልእክት አያያዝ ተግባር
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    # ሒሳብ መፍታት
    if re.match(r'^\d+\s*[\+\-\*/]\s*\d+$', user_message.replace(" ", "")):
        try:
            result = eval(user_message)  # ለቀላል ሒሳብ (ማስጠንቀቂያ፡ eval ለተወሳሳቢ ኮድ አደገኛ ሊሆን ይችላል)
            response = f"ውጤቱ፡ {result}"
        except:
            response = "ይቅርታ፣ ሒሳቡን መፍታት አልቻልኩም። ሌላ ሞክር!"
    # የአየር ሁኔታ ጥያቄ
    elif "አየር ሁኔታ" in user_message:
        city = user_message.replace("የ", "").replace("አየር ሁኔታ", "").strip()
        if city:
            # በተለምዶ እዚህ የአየር ሁኔታ API ጥሪ ይደረጋል። ለምሳሌ ሲሆን ቀላል መልስ እሰጣለሁ።
            response = f"በ{city} ያለው የአየር ሁኔታ ጥሩ ነው ብለን እናስብ! ☀️ ተጨማሪ መረጃ ከፈለግህ ንገረኝ።"
        else:
            response = "እባክህ የከተማውን ስም ጻፍ (ለምሳሌ፣ 'የአዲስ አበባ አየር ሁኔታ')።"
    # ተፈጥሮአዊ መልሶች
    elif "ሰላም" in user_message:
        response = "ሰላም! ዛሬ ጥሩ ነው እንዴ? 😄"
    elif "እንደምን" in user_message or "ምን እየሰራህ" in user_message:
        response = "እዚህ ከሰዎች ጋር እየተወያየሁ ነው! 😎 አንተ ምን እየሰራህ ነው?"
    elif "እርዳኝ" in user_message:
        response = "በእርግጥ! በምን ልረዳህ? /help ተጠቀም ምን ማድረግ እንደምችል ለማየት።"
    else:
        response = "ምንም እንኳን መልእክትህ ሙሉ በሙሉ ባይገባኝም፣ እንደ ጓደኛ ልመልስህ እሞክራለሁ! 😊 ሌላ ምን አለ?"

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
    print("ቦቱ ጀምሯል...")
    app.run_polling()

if __name__ == "__main__":
    main()
