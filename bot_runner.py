#!/usr/bin/env python3
"""
تشغيل البوت مع إعادة التشغيل التلقائي
"""

import os
import sys
import time
import logging

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def run_bot():
    """تشغيل البوت"""
    try:
        # إضافة المسار الحالي
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        from main import main
        logger.info("🚀 بدء تشغيل البوت...")
        main()
        return True
    except KeyboardInterrupt:
        logger.info("👋 تم إيقاف البوت")
        return True
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    logger.info("🎓 بدء نظام بوت الاختبارات")
    
    # التحقق من التوكن
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("""
        ⚠️  **خطأ: التوكن غير موجود**
        
        كيفية الإصلاح:
        1. سجل في https://render.com
        2. اختر خدمتك
        3. اضغط على Environment
        4. أضف متغير بيئة جديد:
           - المفتاح: TELEGRAM_BOT_TOKEN
           - القيمة: التوكن الذي حصلت عليه من @BotFather
        
        للحصول على التوكن:
        1. افتح Telegram
        2. ابحث عن @BotFather
        3. أرسل /newbot
        4. اتبع التعليمات
        """)
        return
    
    logger.info(f"✅ التوكن موجود (يبدأ بـ: {token[:10]}...)")
    logger.info(f"🐍 إصدار Python: {sys.version}")
    
    # تشغيل البوت مع إعادة المحاولة
    max_attempts = 5
    attempt = 1
    
    while attempt <= max_attempts:
        logger.info(f"🔧 المحاولة {attempt}/{max_attempts}")
        
        if run_bot():
            break
        
        wait_time = attempt * 10  # 10, 20, 30, 40, 50 ثانية
        logger.info(f"⏳ إعادة المحاولة بعد {wait_time} ثانية...")
        time.sleep(wait_time)
        attempt += 1
    
    if attempt > max_attempts:
        logger.error("🛑 فشل تشغيل البوت بعد جميع المحاولات")
    else:
        logger.info("✅ تم إنهاء البوت")

if __name__ == "__main__":
    main()
