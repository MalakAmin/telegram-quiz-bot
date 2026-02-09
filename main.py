import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# حالة تخزين بسيطة
quizzes = {}

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(
        f"مرحبًا {user.first_name}! 👋\n\n"
        "🎓 **بوت اختبارات الطلاب**\n\n"
        "✅ /addquiz - إنشاء اختبار جديد\n"
        "📝 /takequiz - أداء اختبار\n"
        "ℹ️ /help - المساعدة\n\n"
        "اختر الأمر المناسب لك!"
    )

async def help_command(update: Update, context: CallbackContext):
    help_text = """
    **أوامر البوت:**
    
    👨‍🏫 **للمعلمين:**
    /addquiz - إنشاء اختبار جديد
    
    👨‍🎓 **للطلاب:**
    /takequiz - أداء اختبار
    
    **عام:**
    /start - بدء المحادثة
    /help - هذه التعليمات
    """
    await update.message.reply_text(help_text)

async def addquiz(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📝 **إنشاء اختبار جديد**\n\n"
        "سيتم تطوير هذه الميزة قريباً!\n"
        "حالياً يمكنك استخدام البوت للتواصل الأساسي."
    )

async def takequiz(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "📝 **الاختبارات**\n\n"
        "لا توجد اختبارات متاحة حالياً.\n"
        "اطلب من معلمك إنشاء اختبار باستخدام /addquiz"
    )

async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    if text.startswith('/'):
        return
    
    await update.message.reply_text(
        "أهلاً! 👋\n"
        "استخدم /help لرؤية الأوامر المتاحة."
    )

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    # الحصول على التوكن
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        logger.error("❌ لم يتم تعيين TELEGRAM_BOT_TOKEN!")
        print("\n🔧 **كيفية إضافة التوكن في Render:**")
        print("1. اذهب إلى Dashboard")
        print("2. اختر خدمتك")
        print("3. اضغط على Environment")
        print("4. أضف: TELEGRAM_BOT_TOKEN = 'توكن_البوت'")
        return
    
    print(f"✅ تم العثور على التوكن: {TOKEN[:10]}...")
    
    # إنشاء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # إضافة handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("addquiz", addquiz))
    application.add_handler(CommandHandler("takequiz", takequiz))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # تشغيل البوت
    print("🤖 بدء تشغيل البوت...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
