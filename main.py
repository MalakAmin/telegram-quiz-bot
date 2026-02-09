import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# التسجيل
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text(
        "👋 أهلاً! أنا بوت الاختبارات.\n"
        "✅ البوت يعمل بشكل صحيح!\n\n"
        "استخدم /help لرؤية الأوامر."
    )

async def help_command(update: Update, context):
    await update.message.reply_text(
        "📋 **الأوامر:**\n"
        "/start - بدء المحادثة\n"
        "/addquiz - إنشاء اختبار\n"
        "/takequiz - أداء اختبار\n"
        "/help - هذه الرسالة"
    )

async def addquiz(update: Update, context):
    await update.message.reply_text(
        "📝 **إنشاء اختبار:**\n"
        "هذه الميزة قيد التطوير.\n"
        "سيتم إضافتها قريباً!"
    )

async def takequiz(update: Update, context):
    await update.message.reply_text(
        "📝 **الاختبارات:**\n"
        "لا توجد اختبارات حالياً."
    )

def main():
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("❌ أضف TELEGRAM_BOT_TOKEN في Environment Variables")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("addquiz", addquiz))
    app.add_handler(CommandHandler("takequiz", takequiz))
    
    print("🤖 البوت يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
