#!/usr/bin/env python3
"""
تشغيل البوت بشكل مستمر
"""

import os
import sys
import time
import logging

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """الدالة الرئيسية"""
    logger.info("🚀 بدء تشغيل بوت الاختبارات")
    
    # التحقق من التوكن
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("""
        ⚠️  **التوكن غير موجود!**
        
        كيفية الإصلاح على Render:
        1. اضغط على اسم الخدمة
        2. اختر Environment
        3. أضف متغير جديد:
           - المفتاح: TELEGRAM_BOT_TOKEN
           - القيمة: توكن البوت من @BotFather
        """)
        return
    
    logger.info(f"✅ التوكن موجود: {token[:10]}...")
    
    # إضافة المسار
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # تشغيل البوت مع إعادة المحاولة
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        try:
            logger.info(f"🔧 المحاولة {attempts + 1}/{max_attempts}")
            
            from main import main as run_bot
            run_bot()
            
        except KeyboardInterrupt:
            logger.info("👋 تم إيقاف البوت")
            break
            
        except Exception as e:
            logger.error(f"❌ خطأ: {e}")
            attempts += 1
            wait = min(30 * attempts, 300)
            logger.info(f"⏳ إعادة التشغيل بعد {wait} ثانية...")
            time.sleep(wait)
    
    if attempts >= max_attempts:
        logger.error("🛑 فشل بعد جميع المحاولات")

if __name__ == "__main__":
    main()
