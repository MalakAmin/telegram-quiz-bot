#!/usr/bin/env python3
"""
بوت تيليجرام مبسط يعمل 100%
"""

import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تخزين البيانات البسيط
quizzes = {}

def start(update: Update, context: CallbackContext):
    """أمر البداية"""
    user = update.effective_user
    text = f"""
👋 أهلاً {user.first_name}!

🎓 **بوت الاختبارات التعليمي**

✅ /addquiz - إنشاء اختبار
📝 /takequiz - أداء اختبار
📚 /myquizzes - اختباراتي
ℹ️ /help - المساعدة

البوت يعمل بشكل صحيح! ✅
    """
    update.message.reply_text(text)

def help_command(update: Update, context: CallbackContext):
    """أمر المساعدة"""
    help_text = """
📋 **الأوامر المتاحة:**

/addquiz - إنشاء اختبار جديد
/takequiz - أداء اختبار
/myquizzes - عرض اختباراتك
/help - هذه الرسالة

👨‍🏫 **لإنشاء اختبار:**
1. استخدم /addquiz
2. اتبع التعليمات

👨‍🎓 **لأداء اختبار:**
1. استخدم /takequiz
2. اختر من القائمة
    """
    update.message.reply_text(help_text)

def addquiz(update: Update, context: CallbackContext):
    """إنشاء اختبار"""
    update.message.reply_text(
        "📝 **إنشاء اختبار جديد**\n\n"
        "هذه الميزة قيد التطوير.\n"
        "حالياً يمكنك استخدام البوت للتواصل الأساسي.\n\n"
        "✅ البوت يعمل بشكل صحيح!"
    )

def takequiz(update: Update, context: CallbackContext):
    """أداء اختبار"""
    update.message.reply_text(
        "📝 **الاختبارات**\n\n"
        "لا توجد اختبارات متاحة حالياً.\n"
        "يمكن للمعلمين إنشاء اختبارات باستخدام /addquiz"
    )

def myquizzes(update: Update, context: CallbackContext):
    """عرض اختباراتي"""
    update.message.reply_text(
        "📚 **اختباراتي**\n\n"
        "لم تنشئ أي اختبارات بعد.\n"
        "استخدم /addquiz لإنشاء أول اختبار لك."
    )

def echo(update: Update, context: CallbackContext):
    """رد على الرسائل العادية"""
    update.message.reply_text(
        "🤖 أنا بوت الاختبارات!\n"
        "استخدم /help لرؤية الأوامر المتاحة."
    )

def main():
    """الدالة الرئيسية"""
    # الحصول على التوكن
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("❌ خطأ: TELEGRAM_BOT_TOKEN غير موجود!")
        print("\n🔧 **أضف التوكن في Render:**")
        print("1. اختر خدمتك")
        print("2. اضغط على Environment")
        print("3. أضف: TELEGRAM_BOT_TOKEN = 'توكنك'")
        return
    
    print(f"✅ التوكن: {TOKEN[:10]}...")
    
    # إنشاء البوت
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # إضافة الأوامر
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("addquiz", addquiz))
    dp.add_handler(CommandHandler("takequiz", takequiz))
    dp.add_handler(CommandHandler("myquizzes", myquizzes))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    # بدء البوت
    print("🤖 البوت يعمل...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
