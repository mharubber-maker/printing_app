import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# التأكد من زرع البوابة الإجبارية
if "app.mount('/static'" not in content and "app.mount(\"/static\"" not in content:
    if "from fastapi.staticfiles import StaticFiles" not in content:
        content = "from fastapi.staticfiles import StaticFiles\n" + content
        
    # حقن كود البوابة أسفل تعريف الـ app مباشرة
    content = re.sub(r"(app\s*=\s*FastAPI\([^)]*\))", r"\1\napp.mount('/static', StaticFiles(directory='static'), name='static')", content)
    
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ تم كسر الحماية الإفتراضية وفتح مسار الصور بنجاح!")
else:
    print("✅ المسار موجود بالفعل.")
