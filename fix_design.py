import os, base64

base = '/home/ghazal/printing_app'

# لو اللوجو موجود
logo_tag = '<span style="font-size:60px;line-height:1">🖨️</span>'
for logo_path in [
    '/home/ghazal/printing_app/static/uploads/logo.jpg',
    '/home/ghazal/Downloads/IMG-20260306-WA0001.jpg',
]:
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        logo_tag = f'<img src="data:image/jpeg;base64,{b64}" style="width:100px;height:100px;border-radius:50%;object-fit:cover;border:3px solid #f5a623;box-shadow:0 0 30px rgba(245,166,35,0.6)">'
        print(f"✅ اللوجو اتحمل من {logo_path}")
        break

files = {}

# ============================================================
files['templates/components/header.html'] = f"""<header style="max-width:960px;margin:0 auto var(--space-5);padding:var(--space-5) var(--space-4);border-radius:var(--radius-xl);background:linear-gradient(135deg,#2d1a00,#1a0f00);position:relative;overflow:hidden">
    <div style="position:absolute;bottom:0;left:0;right:0;height:3px;background:linear-gradient(90deg,#ff0000,#ff8800,#ffff00,#00ff88,#0088ff,#8800ff);background-size:200% 100%;animation:rainbowFlow 3s linear infinite"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;position:relative;z-index:1;gap:16px">

        <!-- العنوان يمين -->
        <div style="text-align:right;flex:1">
            <h1 style="font-size:22px;font-weight:900;color:#ffd700;line-height:1.3">
                نظام إدارة الطلبات
            </h1>
            <p style="font-size:11px;color:rgba(245,166,35,0.6);margin-top:4px">
                بيت الطباعة والألوان
            </p>
        </div>

        <!-- اللوجو وسط -->
        <div style="flex-shrink:0">
            {logo_tag}
        </div>

        <!-- الأزرار شمال -->
        <div style="display:flex;flex-direction:column;gap:8px;align-items:flex-start;flex:1">
            <button onclick="openModal()"
                    style="background:linear-gradient(135deg,#f5a623,#ffd700);color:#1a0f00;font-weight:900;border:none;padding:10px 20px;border-radius:12px;cursor:pointer;font-family:Cairo,sans-serif;font-size:13px;box-shadow:0 4px 15px rgba(245,166,35,0.4);transition:all 0.3s;white-space:nowrap">
                ➕ طلب جديد
            </button>
            <button id="theme-toggle" onclick="toggleTheme()"
                    style="background:rgba(255,255,255,0.1);color:rgba(255,255,255,0.8);border:1px solid rgba(255,255,255,0.2);padding:6px 16px;border-radius:50px;cursor:pointer;font-family:Cairo,sans-serif;font-size:12px;transition:all 0.3s">
                🌙 Dark
            </button>
        </div>

    </div>
</header>"""

# ============================================================
files['templates/partials/stats.html'] = """<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:20px">

    <div style="background:var(--bg-card);border-radius:16px;padding:20px;
                border:1px solid var(--border-color);box-shadow:var(--shadow-sm);
                border-right:4px solid #f5a623;position:relative;overflow:hidden"
         class="anim-fade-up delay-1">
        <div style="font-size:38px;font-weight:900;color:#c9820a;line-height:1">
            {{ stats.total }}
        </div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:6px;font-weight:600">
            إجمالى الطلبات
        </div>
        <div style="position:absolute;left:16px;top:50%;transform:translateY(-50%);font-size:28px;opacity:0.15">
            📊
        </div>
    </div>

    <div style="background:var(--bg-card);border-radius:16px;padding:20px;
                border:1px solid var(--border-color);box-shadow:var(--shadow-sm);
                border-right:4px solid #ff6644;position:relative;overflow:hidden"
         class="anim-fade-up delay-2">
        <div style="font-size:38px;font-weight:900;color:#ff6644;line-height:1">
            {{ stats.ongoing }}
        </div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:6px;font-weight:600">
            طلبات جارية
        </div>
        <div style="position:absolute;left:16px;top:50%;transform:translateY(-50%);font-size:28px;opacity:0.15">
            ⚡
        </div>
    </div>

    <div style="background:var(--bg-card);border-radius:16px;padding:20px;
                border:1px solid var(--border-color);box-shadow:var(--shadow-sm);
                border-right:4px solid #00aa66;position:relative;overflow:hidden"
         class="anim-fade-up delay-3">
        <div style="font-size:38px;font-weight:900;color:#00aa66;line-height:1">
            {{ stats.delivered }}
        </div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:6px;font-weight:600">
            تم التسليم
        </div>
        <div style="position:absolute;left:16px;top:50%;transform:translateY(-50%);font-size:28px;opacity:0.15">
            ✅
        </div>
    </div>

</div>"""

# ============================================================
files['templates/partials/orders_table.html'] = """<div style="background:var(--bg-card);border-radius:16px;overflow:hidden;
            border:1px solid var(--border-color);box-shadow:var(--shadow-sm)">

    <div style="padding:16px 20px;background:linear-gradient(135deg,#2d1a00,#1a0f00);
                display:flex;justify-content:space-between;align-items:center">
        <span style="font-size:15px;font-weight:900;color:#ffd700">
            📋 قائمة الطلبات
        </span>
        <span style="font-size:11px;color:rgba(245,166,35,0.5);
                     background:rgba(245,166,35,0.1);padding:3px 12px;
                     border-radius:50px;border:1px solid rgba(245,166,35,0.2)">
            {{ orders|length }} طلب
        </span>
    </div>

    <table style="width:100%;border-collapse:separate;border-spacing:0;text-align:right">
        <thead>
            <tr style="background:var(--bg-table-head)">
                <th style="padding:10px 16px;font-size:11px;font-weight:700;color:#c9820a">رقم الطلب</th>
                <th style="padding:10px 16px;font-size:11px;font-weight:700;color:#c9820a">العميل</th>
                <th style="padding:10px 16px;font-size:11px;font-weight:700;color:#c9820a">المقاس</th>
                <th style="padding:10px 16px;font-size:11px;font-weight:700;color:#c9820a">المساحة</th>
                <th style="padding:10px 16px;font-size:11px;font-weight:700;color:#c9820a">الحالة</th>
                <th style="padding:10px 16px;font-size:11px;font-weight:700;color:#c9820a">حذف</th>
            </tr>
        </thead>
        <tbody id="orders-table-body">
            {% for order in orders %}
                {% include "partials/order_row.html" %}
            {% else %}
                <tr>
                    <td colspan="6" style="text-align:center;padding:60px 16px;color:var(--text-muted)">
                        <div style="font-size:48px;margin-bottom:12px">📋</div>
                        <div style="font-weight:700;font-size:15px">مفيش طلبات</div>
                        <div style="font-size:12px;margin-top:6px">اضغط طلب جديد للبداية</div>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>"""

# ============================================================
files['templates/partials/order_row.html'] = """<tr id="order-{{ order.id }}"
    style="border-bottom:1px solid var(--border-color);transition:background 0.15s"
    onmouseover="this.style.background='var(--bg-card-hover)'"
    onmouseout="this.style.background=''">

    <td style="padding:12px 16px">
        <div style="font-family:monospace;font-weight:900;font-size:13px;color:#c9820a">
            {{ order.number }}
        </div>
        <div style="font-size:10px;color:var(--text-muted);margin-top:2px">
            📅 {{ order.created_at.strftime("%Y/%m/%d") }}
        </div>
        {% if order.delivery_date %}
        <div style="font-size:10px;color:#ff8844;margin-top:2px">
            🚚 {{ order.delivery_date.strftime("%Y/%m/%d") }}
        </div>
        {% endif %}
    </td>

    <td style="padding:12px 16px">
        <div style="font-weight:700;color:var(--text-primary);font-size:13px">
            {{ order.customer_name }}
        </div>
        {% if order.customer_phone %}
        <div style="font-size:11px;color:var(--text-muted);margin-top:2px">
            📱 {{ order.customer_phone }}
        </div>
        {% endif %}
    </td>

    <td style="padding:12px 16px;font-size:12px;color:var(--text-secondary)">
        {{ order.length }}م × {{ order.width }}م
    </td>

    <td style="padding:12px 16px;font-weight:700;color:#c9820a;font-size:13px">
        {{ order.area_display }} م²
    </td>

    <td style="padding:12px 16px">
        <form hx-post="/orders/{{ order.id }}/status"
              hx-target="#order-{{ order.id }}"
              hx-swap="outerHTML">
            {% set sc = "ongoing" if order.status == "جارى" else "ready" if order.status == "جاهز" else "done" %}
            <select name="new_status"
                    class="status-select badge badge-{{ sc }}"
                    onchange="this.form.requestSubmit()">
                <option value="جارى"        {% if order.status=="جارى" %}selected{% endif %}>جارى</option>
                <option value="جاهز"        {% if order.status=="جاهز" %}selected{% endif %}>جاهز</option>
                <option value="تم التسليم" {% if order.status=="تم التسليم" %}selected{% endif %}>تم التسليم</option>
            </select>
        </form>
    </td>

    <td style="padding:12px 16px">
        <button style="background:none;border:none;cursor:pointer;color:rgba(255,100,100,0.5);font-size:18px;transition:color 0.2s"
                onmouseover="this.style.color='rgba(255,80,80,0.9)'"
                onmouseout="this.style.color='rgba(255,100,100,0.5)'"
                hx-delete="/orders/{{ order.id }}"
                hx-target="#order-{{ order.id }}"
                hx-swap="outerHTML"
                hx-confirm="هتحذف الطلب {{ order.number }}؟">
            🗑️
        </button>
    </td>
</tr>"""

# ============================================================
files['templates/components/search.html'] = """<div style="background:var(--bg-card);border-radius:16px;border:1px solid var(--border-color);
            padding:16px;margin-bottom:16px;box-shadow:var(--shadow-sm)">
    <form method="get" action="/" style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
        <input type="text" name="search" value="{{ search }}"
               placeholder="🔍 ابحث باسم العميل أو رقم الطلب..."
               style="flex:1;min-width:200px;background:var(--bg-input);border:1px solid var(--border-color);
                      border-radius:12px;padding:10px 16px;color:var(--text-primary);
                      font-family:Cairo,sans-serif;font-size:13px;text-align:right;outline:none"
               onfocus="this.style.borderColor='#f5a623'"
               onblur="this.style.borderColor='var(--border-color)'">

        <select name="status"
                style="background:var(--bg-input);border:1px solid var(--border-color);
                       border-radius:12px;padding:10px 12px;color:var(--text-primary);
                       font-family:Cairo,sans-serif;font-size:12px;outline:none;min-width:120px">
            <option value="">كل الحالات</option>
            <option value="جارى"        {% if status=="جارى" %}selected{% endif %}>جارى</option>
            <option value="جاهز"        {% if status=="جاهز" %}selected{% endif %}>جاهز</option>
            <option value="تم التسليم" {% if status=="تم التسليم" %}selected{% endif %}>تم التسليم</option>
        </select>

        <button type="submit"
                style="background:linear-gradient(135deg,#f5a623,#ffd700);color:#1a1008;font-weight:700;
                       border:none;border-radius:12px;padding:10px 20px;cursor:pointer;
                       font-family:Cairo,sans-serif;font-size:13px">
            بحث
        </button>

        {% if search or status %}
        <a href="/"
           style="background:var(--bg-card);color:var(--text-muted);border:1px solid var(--border-color);
                  border-radius:12px;padding:10px 16px;text-decoration:none;font-size:13px">
            مسح
        </a>
        {% endif %}
    </form>
</div>"""

# ============================================================
# كتابة الملفات
for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n') + 1
    print(f"✅ {lines:3d} سطر ← {path}")

print("\n🎉 كل الإصلاحات اتعملت")
print("\nدلوقتى:")
print("  docker compose restart app")