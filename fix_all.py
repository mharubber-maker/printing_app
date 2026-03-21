import os
base = '/home/ghazal/printing_app'
files = {}

files['templates/partials/stats.html'] = """<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:20px">
    <div class="anim-fade-up delay-1" style="border-radius:16px;padding:20px;position:relative;overflow:hidden;background:linear-gradient(135deg,rgba(245,166,35,0.15),rgba(245,166,35,0.05));border:1px solid rgba(245,166,35,0.3)">
        <div style="font-size:42px;font-weight:900;color:#f5a623;line-height:1">{{ stats.total }}</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:8px;font-weight:600">إجمالى الطلبات</div>
        <div style="position:absolute;left:12px;top:50%;transform:translateY(-50%);font-size:32px;opacity:0.2">📊</div>
    </div>
    <div class="anim-fade-up delay-2" style="border-radius:16px;padding:20px;position:relative;overflow:hidden;background:linear-gradient(135deg,rgba(255,102,68,0.15),rgba(255,102,68,0.05));border:1px solid rgba(255,102,68,0.3)">
        <div style="font-size:42px;font-weight:900;color:#ff6644;line-height:1">{{ stats.ongoing }}</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:8px;font-weight:600">طلبات جارية</div>
        <div style="position:absolute;left:12px;top:50%;transform:translateY(-50%);font-size:32px;opacity:0.2">⚡</div>
    </div>
    <div class="anim-fade-up delay-3" style="border-radius:16px;padding:20px;position:relative;overflow:hidden;background:linear-gradient(135deg,rgba(0,170,102,0.15),rgba(0,170,102,0.05));border:1px solid rgba(0,170,102,0.3)">
        <div style="font-size:42px;font-weight:900;color:#00aa66;line-height:1">{{ stats.delivered }}</div>
        <div style="font-size:12px;color:var(--text-muted);margin-top:8px;font-weight:600">تم التسليم</div>
        <div style="position:absolute;left:12px;top:50%;transform:translateY(-50%);font-size:32px;opacity:0.2">✅</div>
    </div>
</div>"""

files['templates/components/search.html'] = """<div style="border-radius:16px;border:1px solid var(--border-color);padding:16px;margin-bottom:16px;background:var(--bg-card)">
    <form method="get" action="/" style="display:flex;gap:10px;flex-wrap:wrap;align-items:center">
        <input type="text" name="search" value="{{ search }}"
               placeholder="🔍 ابحث باسم العميل أو رقم الطلب..."
               style="flex:1;min-width:200px;background:var(--bg-input);border:1px solid var(--border-color);border-radius:12px;padding:10px 16px;color:var(--text-primary);font-family:Cairo,sans-serif;font-size:13px;text-align:right;outline:none;transition:border-color 0.2s"
               onfocus="this.style.borderColor='#f5a623'"
               onblur="this.style.borderColor='var(--border-color)'">
        <select name="status"
                style="background:var(--bg-input);border:1px solid var(--border-color);border-radius:12px;padding:10px 12px;color:var(--text-primary);font-family:Cairo,sans-serif;font-size:12px;outline:none;min-width:130px;cursor:pointer">
            <option value="">كل الحالات</option>
            <option value="جارى" {% if status=="جارى" %}selected{% endif %}>جارى</option>
            <option value="جاهز" {% if status=="جاهز" %}selected{% endif %}>جاهز</option>
            <option value="تم التسليم" {% if status=="تم التسليم" %}selected{% endif %}>تم التسليم</option>
        </select>
        <button type="submit" style="background:linear-gradient(135deg,#f5a623,#ffd700);color:#1a1008;font-weight:900;border:none;border-radius:12px;padding:10px 20px;cursor:pointer;font-family:Cairo,sans-serif;font-size:13px">بحث</button>
        {% if search or status %}
        <a href="/" style="color:var(--text-muted);border:1px solid var(--border-color);border-radius:12px;padding:10px 16px;text-decoration:none;font-size:13px;background:var(--bg-card)">مسح</a>
        {% endif %}
    </form>
</div>"""

files['templates/partials/order_row.html'] = """<tr id="order-{{ order.id }}"
    style="border-bottom:1px solid var(--border-color);transition:background 0.15s"
    onmouseover="this.style.background='var(--bg-card-hover)'"
    onmouseout="this.style.background=''">
    <td style="padding:12px 16px">
        <div style="font-family:monospace;font-weight:900;font-size:13px;color:#f5a623">{{ order.number }}</div>
        <div style="font-size:10px;color:var(--text-muted);margin-top:2px" dir="ltr">{{ order.created_at.strftime("%d/%m/%Y") }}</div>
        {% if order.delivery_date %}
        <div style="font-size:10px;color:#ff8844;margin-top:2px" dir="ltr">🚚 {{ order.delivery_date.strftime("%d/%m/%Y") }}</div>
        {% endif %}
    </td>
    <td style="padding:12px 16px">
        <div style="font-weight:700;color:var(--text-primary);font-size:13px">{{ order.customer_name }}</div>
        {% if order.customer_phone %}
        <div style="font-size:11px;color:var(--text-muted);margin-top:2px" dir="ltr">{{ order.customer_phone }}</div>
        {% endif %}
    </td>
    <td style="padding:12px 16px;font-size:12px;color:var(--text-secondary)">{{ order.length }}م × {{ order.width }}م</td>
    <td style="padding:12px 16px;font-weight:900;color:#f5a623;font-size:14px">{{ order.area_display }} م²</td>
    <td style="padding:12px 16px">
        <form hx-post="/orders/{{ order.id }}/status" hx-target="#order-{{ order.id }}" hx-swap="outerHTML">
            {% set sc = "ongoing" if order.status=="جارى" else "ready" if order.status=="جاهز" else "done" %}
            <select name="new_status" class="status-select badge badge-{{ sc }}" onchange="this.form.requestSubmit()">
                <option value="جارى" {% if order.status=="جارى" %}selected{% endif %}>جارى</option>
                <option value="جاهز" {% if order.status=="جاهز" %}selected{% endif %}>جاهز</option>
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
                hx-confirm="هتحذف الطلب {{ order.number }}؟">🗑️</button>
    </td>
</tr>"""

files['static/css/tokens.css'] = """:root {
    --gold:#f5a623; --gold-dark:#c9820a; --gold-light:#ffd700;
    --gold-glow:rgba(245,166,35,0.4); --gold-subtle:rgba(245,166,35,0.1);
    --font-family:"Cairo",sans-serif;
    --text-xs:11px; --text-sm:13px; --text-base:15px; --text-lg:18px; --text-xl:22px;
    --font-normal:400; --font-bold:700; --font-black:900;
    --space-1:4px; --space-2:8px; --space-3:12px; --space-4:16px; --space-5:20px; --space-6:24px;
    --radius-sm:8px; --radius-md:12px; --radius-lg:16px; --radius-xl:20px; --radius-full:9999px;
    --transition-fast:150ms ease; --transition-base:300ms ease; --transition-slow:500ms ease;
    --shadow-sm:0 2px 8px rgba(0,0,0,0.06); --shadow-md:0 4px 16px rgba(0,0,0,0.10);
    --shadow-lg:0 8px 32px rgba(0,0,0,0.15);
    --shadow-gold:0 4px 20px rgba(245,166,35,0.4);
    --shadow-glow:0 0 30px rgba(245,166,35,0.4);
}
[data-theme="light"] {
    --bg-page:#f5f0e8;
    --bg-card:#ffffff;
    --bg-card-hover:#fdf8f0;
    --bg-table-head:#fdf5e8;
    --bg-input:#ffffff;
    --bg-modal:#ffffff;
    --bg-overlay:rgba(0,0,0,0.5);
    --text-primary:#1a1008;
    --text-secondary:#555555;
    --text-muted:#888888;
    --border-color:#e8d8b8;
    --border-focus:#f5a623;
    --badge-ongoing-bg:#fff8e8; --badge-ongoing-fg:#c9820a; --badge-ongoing-br:#f5d890;
    --badge-ready-bg:#e8fff5;   --badge-ready-fg:#00aa66;   --badge-ready-br:#90f5cc;
    --badge-done-bg:#e8f0ff;    --badge-done-fg:#4466cc;    --badge-done-br:#99aaee;
    --rainbow:linear-gradient(90deg,#ff0000,#ff8800,#ffff00,#00ff88,#0088ff,#8800ff);
}
[data-theme="dark"] {
    --bg-page:#0d0d1a;
    --bg-card:rgba(255,255,255,0.04);
    --bg-card-hover:rgba(255,255,255,0.07);
    --bg-table-head:rgba(0,0,0,0.4);
    --bg-input:rgba(255,255,255,0.06);
    --bg-modal:#0f0f1a;
    --bg-overlay:rgba(0,0,0,0.8);
    --text-primary:#ffffff;
    --text-secondary:rgba(255,255,255,0.65);
    --text-muted:rgba(255,255,255,0.35);
    --border-color:rgba(255,255,255,0.1);
    --border-focus:rgba(245,166,35,0.7);
    --badge-ongoing-bg:rgba(245,166,35,0.15); --badge-ongoing-fg:#f5a623; --badge-ongoing-br:rgba(245,166,35,0.35);
    --badge-ready-bg:rgba(0,200,100,0.15);    --badge-ready-fg:#00dd88;   --badge-ready-br:rgba(0,200,100,0.35);
    --badge-done-bg:rgba(99,102,241,0.15);    --badge-done-fg:#818cf8;    --badge-done-br:rgba(99,102,241,0.35);
    --rainbow:linear-gradient(90deg,#ff0000,#ff8800,#ffff00,#00ff88,#0088ff,#8800ff);
}"""

for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n') + 1
    print(f"✅ {lines:3d} سطر ← {path}")

print("\n🎉 تم — شغّل: docker compose restart app")