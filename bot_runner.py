#!/usr/bin/env python3
"""
تشغيل البوت بشكل مستمر
"""

import os
import sys
import time
from threading import Thread
from main import main

def keep_alive():
    """إبقاء البوت نشطًا"""
    while True:
        print(f"🟢 البوت يعمل - {time.strftime('%Y-%m-%d %H:%M:%S')}")
        time.sleep(300)  # طباعة رسالة كل 5 دقائق

if __name__ == "__main__":
    print("🚀 بدء تشغيل بوت اختبارات الطلاب...")
    
    # التحقق من وجود التوكن
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ خطأ: لم يتم تعيين TELEGRAM_BOT_TOKEN في متغيرات البيئة")
        print("🔧 يرجى إضافة التوكن في إعدادات Render:")
        print("   1. اذهب إلى Dashboard")
        print("   2. اختر خدمتك")
        print("   3. اضغط على Environment")
        print("   4. أضف TELEGRAM_BOT_TOKEN مع قيمة التوكن")
        sys.exit(1)
    
    print("✅ تم العثور على التوكن")
    
    # بدء thread للإبقاء على التشغيل
    keep_alive_thread = Thread(target=keep_alive, daemon=True)
    keep_alive_thread.start()
    
    # تشغيل البوت
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 إيقاف البوت...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        sys.exit(1)
