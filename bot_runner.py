#!/usr/bin/env python3
"""
تشغيل البوت بشكل مستمر - نسخة معدلة
"""

import os
import sys
import time
import logging
from threading import Thread

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_bot():
    """تشغيل البوت"""
    try:
        from main import main
        main()
    except Exception as e:
        logger.error(f"خطأ في تشغيل البوت: {e}", exc_info=True)
        return False
    return True

def keep_alive():
    """إبقاء البوت نشطًا"""
    while True:
        logger.info(f"🟢 البوت يعمل - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(300)

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء تشغيل بوت اختبارات الطلاب...")
    
    # التحقق من وجود التوكن
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ خطأ: لم يتم تعيين TELEGRAM_BOT_TOKEN")
        print("🔧 خطوات الإصلاح:")
        print("   1. اذهب إلى Render Dashboard")
        print("   2. اختر خدمتك")
        print("   3. اضغط على Environment")
        print("   4. أضف TELEGRAM_BOT_TOKEN مع التوكن الخاص بك")
        sys.exit(1)
    
    print(f"✅ تم العثور على التوكن (طول: {len(token)} حرف)")
    
    # بدء thread للإبقاء على التشغيل
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # تشغيل البوت مع إعادة التشغيل التلقائي في حالة الفشل
    restart_delay = 10  # ثواني
    
    while True:
        logger.info("تشغيل البوت...")
        if not run_bot():
            logger.error(f"البوت توقف، إعادة التشغيل بعد {restart_delay} ثانية...")
            time.sleep(restart_delay)
            
            # زيادة وقت الانتظار تدريجياً
            restart_delay = min(restart_delay * 1.5, 300)  # حد أقصى 5 دقائق

if __name__ == "__main__":
    main()
