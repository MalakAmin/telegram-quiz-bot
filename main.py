#!/usr/bin/env python3
"""
بوت تيليجرام لاختبارات الطلاب - الإصدار المستقر
"""

import os
import logging
import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler, MessageHandler,
    Filters, CallbackContext, ConversationHandler
)

# ========== إعدادات ==========
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ملف تخزين البيانات
DATA_FILE = "data.json"

# ========== فئات المحادثة ==========
START, TYPE, TITLE, QUESTION, OPTIONS, ANSWER, MORE = range(7)

# ========== فئة البوت ==========
class QuizBot:
    def __init__(self):
        self.data = self.load_data()
    
    def load_data(self):
        """تحميل البيانات"""
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"quizzes": {}, "teachers": {}, "results": {}}
    
    def save_data(self):
        """حفظ البيانات"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def start_command(self, update: Update, context: CallbackContext):
        """أمر البداية"""
        user = update.effective_user
        text = f"""
👋 مرحباً {user.first_name}!

🎓 **بوت الاختبارات التعليمي**

👨‍🏫 **للمعلمين:**
/addquiz - إنشاء اختبار جديد
/myquizzes - اختباراتي

👨‍🎓 **للطلاب:**
/takequiz - أداء اختبار
/myresults - نتائجي

ℹ️ /help - المساعدة
        """
        update.message.reply_text(text)
        return ConversationHandler.END
    
    def help_command(self, update: Update, context: CallbackContext):
        """أمر المساعدة"""
        help_text = """
📚 **دليل الاستخدام:**

1️⃣ **إنشاء اختبار:**
   - استخدم /addquiz
   - اختر نوع الاختبار
   - أدخل الأسئلة واحدة تلو الأخرى

2️⃣ **أداء اختبار:**
   - استخدم /takequiz
   - اختر من القائمة
   - أجب عن الأسئلة

3️⃣ **عرض النتائج:**
   - /myresults للطلاب
   - /myquizzes للمعلمين

❓ للمساعدة: @malakadmin
        """
        update.message.reply_text(help_text)
    
    def addquiz_start(self, update: Update, context: CallbackContext):
        """بدء إنشاء اختبار"""
        keyboard = [
            [InlineKeyboardButton("صح/خطأ ✅❌", callback_data='truefalse')],
            [InlineKeyboardButton("اختيار متعدد 🔠", callback_data='multiple')]
        ]
        update.message.reply_text(
            "📝 **إنشاء اختبار جديد**\n\n"
            "اختر نوع الاختبار:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # تهيئة البيانات
        context.user_data['quiz'] = {
            'title': '',
            'type': '',
            'questions': [],
            'teacher': update.effective_user.first_name,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        context.user_data['step'] = 0
        
        return TYPE
    
    def set_quiz_type(self, update: Update, context: CallbackContext):
        """تحديد نوع الاختبار"""
        query = update.callback_query
        query.answer()
        
        quiz_type = query.data
        context.user_data['quiz']['type'] = quiz_type
        
        query.edit_message_text(
            "🎯 **الخطوة 1 من 3**\n"
            "أدخل عنوان الاختبار:\n"
            "مثال: 'اختبار الرياضيات - الفصل الأول'"
        )
        
        return TITLE
    
    def set_quiz_title(self, update: Update, context: CallbackContext):
        """تحديد عنوان الاختبار"""
        title = update.message.text
        context.user_data['quiz']['title'] = title
        
        update.message.reply_text(
            f"✅ العنوان: **{title}**\n\n"
            "🎯 **الخطوة 2 من 3**\n"
            "أدخل السؤال الأول:"
        )
        
        return QUESTION
    
    def add_question(self, update: Update, context: CallbackContext):
        """إضافة سؤال"""
        question_text = update.message.text
        
        if 'current_question' not in context.user_data:
            # سؤال جديد
            context.user_data['current_question'] = {
                'text': question_text,
                'options': []
            }
            
            if context.user_data['quiz']['type'] == 'truefalse':
                keyboard = [
                    [InlineKeyboardButton("صح ✅", callback_data='true')],
                    [InlineKeyboardButton("خطأ ❌", callback_data='false')]
                ]
                update.message.reply_text(
                    f"❓ **السؤال:** {question_text}\n\n"
                    "اختر الإجابة الصحيحة:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return ANSWER
            else:
                update.message.reply_text(
                    f"❓ **السؤال:** {question_text}\n\n"
                    "أدخل الخيار الأول (أ):"
                )
                return OPTIONS
        else:
            # إضافة خيارات متعددة
            context.user_data['current_question']['options'].append(update.message.text)
            options_count = len(context.user_data['current_question']['options'])
            
            if options_count < 4:
                option_names = ['ب', 'ج', 'د']
                update.message.reply_text(f"أدخل الخيار {option_names[options_count-1]}:")
                return OPTIONS
            else:
                keyboard = [
                    [InlineKeyboardButton("أ", callback_data='0')],
                    [InlineKeyboardButton("ب", callback_data='1')],
                    [InlineKeyboardButton("ج", callback_data='2')],
                    [InlineKeyboardButton("د", callback_data='3')]
                ]
                
                options = context.user_data['current_question']['options']
                text = f"❓ **السؤال:** {context.user_data['current_question']['text']}\n\n"
                text += "**الخيارات:**\n"
                for i, opt in enumerate(options):
                    text += f"{chr(1570+i)}. {opt}\n"
                
                update.message.reply_text(
                    text + "\nاختر الإجابة الصحيحة:",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return ANSWER
    
    def set_answer(self, update: Update, context: CallbackContext):
        """تحديد الإجابة الصحيحة"""
        query = update.callback_query
        query.answer()
        
        # حفظ السؤال السابق
        question = context.user_data['current_question']
        
        if context.user_data['quiz']['type'] == 'truefalse':
            question['correct'] = (query.data == 'true')
        else:
            question['correct'] = int(query.data)
        
        context.user_data['quiz']['questions'].append(question)
        del context.user_data['current_question']
        
        keyboard = [
            [InlineKeyboardButton("نعم، أضف سؤالاً آخر ➕", callback_data='yes')],
            [InlineKeyboardButton("لا، انتهيت ✅", callback_data='no')]
        ]
        
        query.edit_message_text(
            f"✅ تم إضافة السؤال!\n\n"
            f"📊 الأسئلة المضافة: {len(context.user_data['quiz']['questions'])}\n\n"
            "هل تريد إضافة سؤال آخر؟",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        return MORE
    
    def handle_more(self, update: Update, context: CallbackContext):
        """معالجة اختيار المزيد"""
        query = update.callback_query
        query.answer()
        
        if query.data == 'yes':
            query.edit_message_text("أدخل السؤال التالي:")
            return QUESTION
        else:
            # حفظ الاختبار
            quiz = context.user_data['quiz']
            user_id = str(update.effective_user.id)
            quiz_id = f"quiz_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            if 'quizzes' not in self.data:
                self.data['quizzes'] = {}
            self.data['quizzes'][quiz_id] = quiz
            
            if user_id not in self.data['teachers']:
                self.data['teachers'][user_id] = []
            self.data['teachers'][user_id].append(quiz_id)
            
            self.save_data()
            
            query.edit_message_text(
                f"🎉 **تم إنشاء الاختبار بنجاح!**\n\n"
                f"📚 **العنوان:** {quiz['title']}\n"
                f"📊 **النوع:** {'صح/خطأ' if quiz['type'] == 'truefalse' else 'اختيار متعدد'}\n"
                f"❓ **عدد الأسئلة:** {len(quiz['questions'])}\n"
                f"👨‍🏫 **المعلم:** {quiz['teacher']}\n"
                f"📅 **التاريخ:** {quiz['date']}\n\n"
                f"🆔 **كود الاختبار:** `{quiz_id}`\n\n"
                "✅ يمكن للطلاب الآن استخدام /takequiz"
            )
            
            context.user_data.clear()
            return ConversationHandler.END
    
    def cancel(self, update: Update, context: CallbackContext):
        """إلغاء العملية"""
        update.message.reply_text("تم الإلغاء.")
        context.user_data.clear()
        return ConversationHandler.END
    
    def my_quizzes(self, update: Update, context: CallbackContext):
        """عرض اختبارات المعلم"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.data.get('teachers', {}):
            update.message.reply_text("📭 لم تنشئ أي اختبارات بعد.")
            return
        
        quizzes = self.data['teachers'][user_id]
        text = "📚 **اختباراتي:**\n\n"
        
        for i, quiz_id in enumerate(quizzes[:5], 1):
            quiz = self.data['quizzes'].get(quiz_id, {})
            if quiz:
                text += f"{i}. **{quiz.get('title', 'بدون عنوان')}**\n"
                text += f"   📝 {len(quiz.get('questions', []))} سؤال\n"
                text += f"   📅 {quiz.get('date', '')}\n"
                text += f"   🆔 `{quiz_id[:15]}...`\n\n"
        
        update.message.reply_text(text)
    
    def take_quiz(self, update: Update, context: CallbackContext):
        """عرض الاختبارات المتاحة"""
        if not self.data.get('quizzes'):
            update.message.reply_text("📭 لا توجد اختبارات متاحة حالياً.")
            return
        
        quizzes = list(self.data['quizzes'].items())[:10]
        keyboard = []
        
        for quiz_id, quiz in quizzes:
            title = quiz.get('title', 'بدون عنوان')[:30]
            button_text = f"{title} ({len(quiz.get('questions', []))} سؤال)"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"take_{quiz_id}")])
        
        update.message.reply_text(
            "📝 **الاختبارات المتاحة:**\n\n"
            "اختر اختباراً:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ========== الدالة الرئيسية ==========
def main():
    """تشغيل البوت"""
    # الحصول على التوكن
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("❌ خطأ: لم يتم تعيين TELEGRAM_BOT_TOKEN")
        print("\n🔧 **لإصلاح المشكلة:**")
        print("1. اذهب إلى Render Dashboard")
        print("2. اختر خدمتك")
        print("3. اضغط على Environment")
        print("4. أضف متغير:")
        print("   Key: TELEGRAM_BOT_TOKEN")
        print("   Value: التوكن من @BotFather")
        return
    
    print(f"✅ تم العثور على التوكن (يبدأ بـ: {TOKEN[:10]}...)")
    
    # إنشاء البوت
    bot = QuizBot()
    
    # إنشاء Updater
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # محادثة إنشاء الاختبار
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addquiz', bot.addquiz_start)],
        states={
            TYPE: [CallbackQueryHandler(bot.set_quiz_type, pattern='^(truefalse|multiple)$')],
            TITLE: [MessageHandler(Filters.text & ~Filters.command, bot.set_quiz_title)],
            QUESTION: [MessageHandler(Filters.text & ~Filters.command, bot.add_question)],
            OPTIONS: [MessageHandler(Filters.text & ~Filters.command, bot.add_question)],
            ANSWER: [CallbackQueryHandler(bot.set_answer)],
            MORE: [CallbackQueryHandler(bot.handle_more, pattern='^(yes|no)$')],
        },
        fallbacks=[CommandHandler('cancel', bot.cancel)]
    )
    
    # إضافة Handlers
    dp.add_handler(CommandHandler("start", bot.start_command))
    dp.add_handler(CommandHandler("help", bot.help_command))
    dp.add_handler(CommandHandler("myquizzes", bot.my_quizzes))
    dp.add_handler(CommandHandler("takequiz", bot.take_quiz))
    dp.add_handler(conv_handler)
    
    # بدء البوت
    print("🤖 بدء تشغيل البوت...")
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
