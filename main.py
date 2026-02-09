import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from datetime import datetime
import json

# تمكين التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# حالات المحادثة
CHOOSING, ADD_QUESTION, ADD_CORRECT_ANSWER, ADD_OPTIONS, ADD_TRUEFALSE, TITLE, VIEW_QUESTIONS = range(7)

# ملف التخزين
DATA_FILE = "quiz_data.json"

class QuizBot:
    def __init__(self, token):
        self.token = token
        self.quizzes = self.load_data()
        
    def load_data(self):
        """تحميل البيانات من الملف"""
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"quizzes": {}, "teachers": {}}
    
    def save_data(self):
        """حفظ البيانات إلى الملف"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.quizzes, f, ensure_ascii=False, indent=2)
    
    async def start(self, update: Update, context: CallbackContext):
        """بدء المحادثة"""
        user = update.effective_user
        await update.message.reply_text(
            f"مرحبًا {user.first_name}! 👋\n\n"
            "🎓 **نظام اختبار الطلاب**\n\n"
            "👨‍🏫 للمعلمين:\n"
            "✅ /addquiz - إضافة اختبار جديد\n"
            "📋 /myquizzes - عرض اختباراتي\n"
            "👨‍🎓 للطلاب:\n"
            "📝 /takequiz - أداء اختبار\n"
            "ℹ️ /help - المساعدة"
        )
        return ConversationHandler.END
    
    async def help_command(self, update: Update, context: CallbackContext):
        """عرض التعليمات"""
        help_text = """
        **دليل استخدام البوت:**
        
        **👨‍🏫 للمعلم:**
        1. استخدم /addquiz لإنشاء اختبار جديد
        2. اختر نوع الاختبار (صح/خطأ أو خيارات)
        3. أدخل الأسئلة خطوة بخطوة
        4. حدد الإجابة الصحيحة
        
        **👨‍🎓 للطالب:**
        1. استخدم /takequiz لعرض الاختبارات المتاحة
        2. اختر الاختبار الذي تريد أداءه
        3. أجب عن الأسئلة واحصل على النتيجة
        
        **أوامر أخرى:**
        /start - إعادة التشغيل
        /myquizzes - عرض اختباراتك (للمعلم)
        /help - عرض هذه التعليمات
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def add_quiz_start(self, update: Update, context: CallbackContext):
        """بدء إضافة اختبار جديد"""
        user_id = str(update.effective_user.id)
        
        keyboard = [
            [InlineKeyboardButton("صح/خطأ", callback_data='truefalse')],
            [InlineKeyboardButton("اختيار من متعدد", callback_data='multiple')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "📝 **إنشاء اختبار جديد**\n\n"
            "أولاً، اختر نوع الاختبار:",
            reply_markup=reply_markup
        )
        
        context.user_data['quiz_creator'] = user_id
        context.user_data['quiz'] = {
            'questions': [],
            'created_at': datetime.now().isoformat(),
            'title': '',
            'type': ''
        }
        
        return TITLE
    
    async def set_quiz_type(self, update: Update, context: CallbackContext):
        """تحديد نوع الاختبار"""
        query = update.callback_query
        await query.answer()
        
        quiz_type = query.data
        context.user_data['quiz']['type'] = quiz_type
        
        await query.edit_message_text(
            "🎯 **الخطوة 1/3**\n"
            "أدخل عنوان الاختبار (مثال: اختبار الرياضيات - الفصل الأول):"
        )
        
        return ADD_QUESTION
    
    async def set_quiz_title(self, update: Update, context: CallbackContext):
        """تحديد عنوان الاختبار"""
        title = update.message.text
        context.user_data['quiz']['title'] = title
        
        await update.message.reply_text(
            f"✅ تم حفظ العنوان: **{title}**\n\n"
            "🎯 **الخطوة 2/3**\n"
            "الآن أدخل السؤال الأول:"
        )
        
        return ADD_QUESTION
    
    async def add_question(self, update: Update, context: CallbackContext):
        """إضافة سؤال جديد"""
        question_text = update.message.text
        
        if 'temp_question' not in context.user_data:
            context.user_data['temp_question'] = {'text': question_text}
            
            if context.user_data['quiz']['type'] == 'truefalse':
                keyboard = [
                    [InlineKeyboardButton("صح", callback_data='true')],
                    [InlineKeyboardButton("خطأ", callback_data='false')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"❓ **السؤال:** {question_text}\n\n"
                    "اختر الإجابة الصحيحة:",
                    reply_markup=reply_markup
                )
                return ADD_TRUEFALSE
            else:
                await update.message.reply_text(
                    f"❓ **السؤال:** {question_text}\n\n"
                    "الآن أدخل الخيار الأول:"
                )
                context.user_data['temp_question']['options'] = []
                return ADD_OPTIONS
        else:
            # إضافة خيارات للأسئلة متعددة الخيارات
            context.user_data['temp_question']['options'].append(update.message.text)
            options_count = len(context.user_data['temp_question']['options'])
            
            if options_count < 4:
                await update.message.reply_text(f"أدخل الخيار {options_count + 1}:")
                return ADD_OPTIONS
            else:
                keyboard = [
                    [InlineKeyboardButton("أ", callback_data='0')],
                    [InlineKeyboardButton("ب", callback_data='1')],
                    [InlineKeyboardButton("ج", callback_data='2')],
                    [InlineKeyboardButton("د", callback_data='3')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                options_text = "\n".join([f"{chr(1570+i)}. {opt}" for i, opt in enumerate(context.user_data['temp_question']['options'])])
                
                await update.message.reply_text(
                    f"❓ **السؤال:** {context.user_data['temp_question']['text']}\n\n"
                    f"**الخيارات:**\n{options_text}\n\n"
                    "اختر رقم الإجابة الصحيحة:",
                    reply_markup=reply_markup
                )
                return ADD_CORRECT_ANSWER
    
    async def add_truefalse_answer(self, update: Update, context: CallbackContext):
        """إضافة إجابة لسؤال صح/خطأ"""
        query = update.callback_query
        await query.answer()
        
        correct_answer = query.data == 'true'
        question = context.user_data['temp_question']
        question['correct'] = correct_answer
        
        context.user_data['quiz']['questions'].append(question)
        del context.user_data['temp_question']
        
        keyboard = [
            [InlineKeyboardButton("نعم، أضف سؤالًا آخر", callback_data='add_more')],
            [InlineKeyboardButton("لا، انتهيت", callback_data='finish')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"✅ تم إضافة السؤال!\n\n"
            "هل تريد إضافة سؤال آخر؟",
            reply_markup=reply_markup
        )
        
        return CHOOSING
    
    async def add_multiple_answer(self, update: Update, context: CallbackContext):
        """إضافة إجابة لسؤال متعدد الخيارات"""
        query = update.callback_query
        await query.answer()
        
        correct_index = int(query.data)
        question = context.user_data['temp_question']
        question['correct'] = correct_index
        
        context.user_data['quiz']['questions'].append(question)
        del context.user_data['temp_question']
        
        keyboard = [
            [InlineKeyboardButton("نعم، أضف سؤالًا آخر", callback_data='add_more')],
            [InlineKeyboardButton("لا، انتهيت", callback_data='finish')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            f"✅ تم إضافة السؤال!\n\n"
            "هل تريد إضافة سؤال آخر؟",
            reply_markup=reply_markup
        )
        
        return CHOOSING
    
    async def handle_choice(self, update: Update, context: CallbackContext):
        """معالجة اختيار المستخدم"""
        query = update.callback_query
        await query.answer()
        
        if query.data == 'add_more':
            await query.edit_message_text("أدخل السؤال التالي:")
            return ADD_QUESTION
        else:  # finish
            quiz = context.user_data['quiz']
            user_id = context.user_data['quiz_creator']
            
            # حفظ الاختبار
            quiz_id = f"quiz_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            if 'quizzes' not in self.quizzes:
                self.quizzes['quizzes'] = {}
            
            self.quizzes['quizzes'][quiz_id] = quiz
            
            # ربط الاختبار بالمعلم
            if user_id not in self.quizzes['teachers']:
                self.quizzes['teachers'][user_id] = []
            self.quizzes['teachers'][user_id].append(quiz_id)
            
            self.save_data()
            
            await query.edit_message_text(
                f"🎉 **تم إنشاء الاختبار بنجاح!**\n\n"
                f"📚 **العنوان:** {quiz['title']}\n"
                f"📊 **نوع الاختبار:** {'صح/خطأ' if quiz['type'] == 'truefalse' else 'اختيار من متعدد'}\n"
                f"❓ **عدد الأسئلة:** {len(quiz['questions'])}\n"
                f"🆔 **كود الاختبار:** `{quiz_id}`\n\n"
                "يمكن للطلاب الآن استخدام /takequiz لأداء الاختبار."
            )
            
            # تنظيف بيانات المستخدم
            context.user_data.clear()
            return ConversationHandler.END
    
    async def cancel(self, update: Update, context: CallbackContext):
        """إلغاء العملية"""
        await update.message.reply_text("تم الإلغاء.")
        context.user_data.clear()
        return ConversationHandler.END
    
    async def my_quizzes(self, update: Update, context: CallbackContext):
        """عرض اختبارات المعلم"""
        user_id = str(update.effective_user.id)
        
        if user_id not in self.quizzes.get('teachers', {}):
            await update.message.reply_text("لم تقم بإنشاء أي اختبارات بعد.")
            return
        
        quiz_ids = self.quizzes['teachers'][user_id]
        quizzes_info = []
        
        for i, quiz_id in enumerate(quiz_ids[:10], 1):  # عرض أول 10 اختبارات
            quiz = self.quizzes['quizzes'].get(quiz_id)
            if quiz:
                quizzes_info.append(
                    f"{i}. **{quiz['title']}**\n"
                    f"   🆔: `{quiz_id}`\n"
                    f"   📝: {len(quiz['questions'])} أسئلة\n"
                    f"   📅: {quiz['created_at'][:10]}"
                )
        
        await update.message.reply_text(
            "📚 **اختباراتي:**\n\n" + "\n\n".join(quizzes_info) if quizzes_info else "لا توجد اختبارات",
            parse_mode='Markdown'
        )
    
    async def take_quiz(self, update: Update, context: CallbackContext):
        """أداء اختبار"""
        if not self.quizzes.get('quizzes'):
            await update.message.reply_text("لا توجد اختبارات متاحة حالياً.")
            return
        
        keyboard = []
        for quiz_id, quiz in list(self.quizzes['quizzes'].items())[:20]:  # عرض أول 20 اختبار
            button_text = f"{quiz['title'][:30]}... ({len(quiz['questions'])} سؤال)"
            keyboard.append([InlineKeyboardButton(button_text, callback_data=f"take_{quiz_id}")])
        
        if not keyboard:
            await update.message.reply_text("لا توجد اختبارات متاحة حالياً.")
            return
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "📝 **الاختبارات المتاحة:**\n\n"
            "اختر اختباراً لأدائه:",
            reply_markup=reply_markup
        )

def main():
    """الدالة الرئيسية لتشغيل البوت"""
    # الحصول على التوكن من متغير البيئة
    TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    if not TOKEN:
        print("⚠️  لم يتم تعيين التوكن! يرجى تعيين متغير البيئة TELEGRAM_BOT_TOKEN")
        return
    
    # إنشاء كائن البوت
    quiz_bot = QuizBot(TOKEN)
    
    # إنشاء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # تعريف handler المحادثة
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addquiz', quiz_bot.add_quiz_start)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_bot.set_quiz_title)],
            ADD_QUESTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_bot.add_question),
                CallbackQueryHandler(quiz_bot.set_quiz_type, pattern='^(truefalse|multiple)$')
            ],
            ADD_OPTIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, quiz_bot.add_question)],
            ADD_TRUEFALSE: [CallbackQueryHandler(quiz_bot.add_truefalse_answer, pattern='^(true|false)$')],
            ADD_CORRECT_ANSWER: [CallbackQueryHandler(quiz_bot.add_multiple_answer, pattern='^[0-3]$')],
            CHOOSING: [CallbackQueryHandler(quiz_bot.handle_choice, pattern='^(add_more|finish)$')],
        },
        fallbacks=[CommandHandler('cancel', quiz_bot.cancel)]
    )
    
    # إضافة الhandlers
    application.add_handler(CommandHandler("start", quiz_bot.start))
    application.add_handler(CommandHandler("help", quiz_bot.help_command))
    application.add_handler(CommandHandler("myquizzes", quiz_bot.my_quizzes))
    application.add_handler(CommandHandler("takequiz", quiz_bot.take_quiz))
    application.add_handler(conv_handler)
    
    # تشغيل البوت
    print("🤖 البوت يعمل...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
