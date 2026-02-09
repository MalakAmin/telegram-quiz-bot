import os
import time
from main import main

if __name__ == "__main__":
    print("🚀 بدء البوت...")
    while True:
        try:
            main()
        except Exception as e:
            print(f"❌ خطأ: {e}")
            print("🔄 إعادة التشغيل بعد 10 ثوان...")
            time.sleep(10)
