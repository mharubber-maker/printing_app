path = "templates/pdf/invoice.html"
try:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    button_code = """
    <style>
        @media print {
            .no-print { display: none !important; }
            body { background: white !important; }
        }
        .print-btn {
            position: fixed; top: 20px; left: 20px;
            background: #f5a623; color: #1a0f00;
            border: none; padding: 10px 20px;
            font-size: 16px; font-weight: bold; font-family: monospace;
            border-radius: 8px; cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            z-index: 1000; transition: all 0.2s;
        }
        .print-btn:hover { background: #ffb732; transform: scale(1.05); }
    </style>
    <button class="no-print print-btn" onclick="window.print()">🖨️ طباعة / حفظ كـ PDF</button>
    """
    
    if "print-btn" not in content:
        # حقن الزر مباشرة بعد فتح وسم body
        content = content.replace("<body>", "<body>\n" + button_code)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ تم إضافة زر الطباعة للفاتورة بنجاح!")
    else:
        print("⚠️ الزر موجود مسبقاً.")
except Exception as e:
    print(f"❌ خطأ: {e}")
