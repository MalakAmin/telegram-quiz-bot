#!/usr/bin/env python3
"""
تشغيل البوت مع مراقبة الأخطاء
"""

import os
import sys
import time

print("🚀 بدء تشغيل بوت تيليجرام...")
print(f"🐍 إصدار Python: {sys.version}")

# التأكد من التوكن
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TOKEN:
    print("❌ خطأ: TELEGRAM_BOT_TOKEN غير موجود!")
    print("أضفه في Environment Variables على Render")
    sys.exit(1)

print(f"✅ التوكن موجود: {TOKEN[:10]}...")

# إضافة المسار
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# محاولات متعددة
max_attempts = 5
for attempt in range(1, max_attempts + 1):
    print(f"\n🔧 المحاولة {attempt}/{max_attempts}")
    
    try:
        from main import main
        main()
        break
        
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف البوت")
        break
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
        
        if attempt < max_attempts:
            wait_time = attempt * 10
            print(f"⏳ إعادة التشغيل بعد {wait_time} ثانية...")
            time.sleep(wait_time)
        else:
            print(f"🛑 فشل بعد {max_attempts} محاولات")

print("\n✅ انتهى تشغيل البوت")
