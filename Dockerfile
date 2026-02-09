# استخدام Python 3.9 - الإصدار المستقر
FROM python:3.9-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ الملفات
COPY requirements.txt .
COPY main.py .
COPY bot_runner.py .
COPY data.json .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# تشغيل البوت
CMD ["python", "bot_runner.py"]
