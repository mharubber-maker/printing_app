import os
from dotenv import load_dotenv

# تحميل الإعدادات من ملف .env
load_dotenv()

# سحب المتغيرات من الملف
APP_NAME = os.getenv("APP_NAME", "بيت الطباعة والألوان")
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "static/uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 5242880))

if __name__ == "__main__":
    print(f"🚀 تم تشغيل تطبيق: {APP_NAME}")
    print(f"🛠️ وضع المطور (Debug): {DEBUG}")
    print(f"📂 مسار الرفع: {UPLOAD_DIR}")
    # هنا تقدر تكمل كود التشغيل بتاعك (FastAPI أو Flask)
