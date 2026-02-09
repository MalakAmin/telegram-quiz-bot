import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context):
    await update.message.reply_text('مرحباً! أنا بوت الاختبارات. استخدم /addquiz لإنشاء اختبار.')

async def addquiz(update: Update, context):
    await update.message.reply_text('سيتم إضافة اختبار قريباً...')

def main():
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("❌ أضف TELEGRAM_BOT_TOKEN في Render Environment")
        return
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addquiz", addquiz))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
    
    print("🤖 البوت يعمل...")
    app.run_polling()

if __name__ == '__main__':
    main()
