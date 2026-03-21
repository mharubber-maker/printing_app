import os, base64
base = '/home/ghazal/printing_app'

# لو اللوجو موجود
logo_tag = '<span style="font-size:50px">🖨️</span>'
logo_path = '/home/ghazal/printing_app/static/uploads/logo.jpg'
if os.path.exists(logo_path):
    with open(logo_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    logo_tag = f'<img src="data:image/jpeg;base64,{b64}" class="logo-ring" style="width:90px;height:90px">'

files = {}

# ============================================================
files['templates/base.html'] = """<!DOCTYPE html>
<html lang="ar" dir="rtl" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}بيت الطباعة والألوان{% endblock %}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/tokens.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <link rel="stylesheet" href="/static/css/components.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% block header %}
        {% include "components/header.html" %}
    {% endblock %}

    <main style="max-width:960px;margin:0 auto;padding:0 var(--space-4) var(--space-4)">
        {% block content %}{% endblock %}
    </main>

    {% include "components/toast.html" %}
    {% include "components/modal.html" %}

    <script src="/static/js/theme.js"></script>
    <script src="/static/js/modal.js"></script>
    <script src="/static/js/utils.js"></script>
    <script src="/static/js/core.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>"""

# ============================================================
files['templates/pages/dashboard.html'] = """{% extends "base.html" %}
{% block title %}لوحة التحكم — بيت الطباعة{% endblock %}

{% block content %}

    <div id="stats-section">
        {% include "partials/stats.html" %}
    </div>

    {% include "components/search.html" %}

    <div id="table-section">
        {% include "partials/orders_table.html" %}
    </div>

{% endblock %}"""

# ============================================================
files['templates/components/header.html'] = f"""<header style="max-width:960px;margin:0 auto var(--space-5);padding:var(--space-5) var(--space-4);border-radius:var(--radius-xl);background:linear-gradient(135deg,#2d1a00,#1a0f00);position:relative;overflow:hidden">
    <div class="rainbow-bar" style="position:absolute;bottom:0;left:0;right:0"></div>
    <div style="display:flex;justify-content:space-between;align-items:center;position:relative;z-index:1">

        <div style="text-align:right">
            <h1 style="font-size:var(--text-xl);font-weight:var(--font-black);color:var(--gold-light);line-height:1.3">
                نظام إدارة الطلبات
            </h1>
            <p style="font-size:var(--text-xs);color:rgba(245,166,35,0.6);margin-top:4px">
                بيت الطباعة والألوان
            </p>
        </div>

        <div style="display:flex;flex-direction:column;align-items:center">
            {logo_tag}
        </div>

        <div style="display:flex;flex-direction:column;gap:var(--space-2);align-items:flex-start">
            <button class="btn btn-primary" onclick="openModal()">
                ➕ طلب جديد
            </button>
            <button id="theme-toggle" class="btn" onclick="toggleTheme()"
                    style="background:rgba(255,255,255,0.1);color:white;font-size:var(--text-xs);padding:6px 14px;border:1px solid rgba(255,255,255,0.2)">
                🌙 Dark
            </button>
        </div>

    </div>
</header>"""

# ============================================================
files['templates/components/search.html'] = """<div class="card" style="padding:var(--space-4);margin-bottom:var(--space-4)">
    <form method="get" action="/" style="display:flex;gap:var(--space-2);flex-wrap:wrap">
        <input type="text" name="search" value="{{ search }}"
               placeholder="🔍 ابحث باسم العميل أو رقم الطلب..."
               class="form-input" style="flex:1;min-width:200px">
        <select name="status" class="form-input" style="width:auto;min-width:130px">
            <option value="">كل الحالات</option>
            <option value="جارى"        {% if status=="جارى" %}selected{% endif %}>جارى</option>
            <option value="جاهز"        {% if status=="جاهز" %}selected{% endif %}>جاهز</option>
            <option value="تم التسليم" {% if status=="تم التسليم" %}selected{% endif %}>تم التسليم</option>
        </select>
        <button type="submit" class="btn btn-primary">بحث</button>
        {% if search or status %}
        <a href="/" class="btn"
           style="background:var(--bg-card);color:var(--text-muted);border:1px solid var(--border-color);text-decoration:none">
            مسح
        </a>
        {% endif %}
    </form>
</div>"""

# ============================================================
files['templates/components/modal.html'] = """<div id="main-modal" class="modal-overlay hidden">
    <div class="modal-card">

        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:var(--space-5)">
            <h2 style="font-size:var(--text-lg);font-weight:var(--font-black);color:var(--text-primary)">
                ➕ طلب جديد
            </h2>
            <button onclick="closeModal()"
                    style="background:none;border:none;cursor:pointer;font-size:22px;color:var(--text-muted);line-height:1">
                ✕
            </button>
        </div>

        <form id="order-form"
              hx-post="/orders/add"
              hx-target="#orders-table-body"
              hx-swap="afterbegin"
              hx-encoding="multipart/form-data"
              style="display:flex;flex-direction:column;gap:var(--space-4)">

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-3)">
                <div>
                    <label class="form-label">اسم العميل *</label>
                    <input name="customer_name" type="text" required
                           placeholder="أحمد محمد" class="form-input">
                </div>
                <div>
                    <label class="form-label">رقم التليفون</label>
                    <input name="customer_phone" type="tel"
                           placeholder="01012345678" class="form-input">
                </div>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-3)">
                <div>
                    <label class="form-label">الطول (م) *</label>
                    <input id="length-input" name="length" type="number"
                           step="0.1" min="0.1" placeholder="3" required class="form-input">
                </div>
                <div>
                    <label class="form-label">العرض (م) *</label>
                    <input id="width-input" name="width" type="number"
                           step="0.1" min="0.1" placeholder="4" required class="form-input">
                </div>
            </div>

            <div style="background:var(--gold-subtle);border:1px solid rgba(245,166,35,0.2);
                        border-radius:var(--radius-md);padding:var(--space-4);text-align:center">
                <p style="font-size:var(--text-xs);color:var(--text-muted)">المساحة المحسوبة</p>
                <p id="area-result"
                   style="font-size:28px;font-weight:var(--font-black);color:var(--gold-dark)">
                    -- م²
                </p>
            </div>

            <div style="display:grid;grid-template-columns:1fr 1fr;gap:var(--space-3)">
                <div>
                    <label class="form-label">تاريخ التسليم</label>
                    <input name="delivery_date" type="date" class="form-input">
                </div>
                <div>
                    <label class="form-label">صورة الطلب</label>
                    <input name="image" type="file" accept="image/*"
                           class="form-input" style="padding:6px 12px">
                </div>
            </div>

            <div>
                <label class="form-label">ملاحظات</label>
                <textarea name="notes" rows="2" placeholder="أى تفاصيل..."
                          class="form-input" style="resize:none"></textarea>
            </div>

            <button type="submit" class="btn btn-primary"
                    style="width:100%;justify-content:center;padding:12px;font-size:var(--text-base)">
                💾 حفظ الطلب
            </button>
        </form>
    </div>
</div>"""

# ============================================================
files['templates/components/toast.html'] = """<div id="toast" class="toast hidden"></div>"""

# ============================================================
files['templates/partials/stats.html'] = """<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-3);margin-bottom:var(--space-4)">
    <div class="stat-card card anim-fade-up delay-1"
         style="border-right:3px solid var(--gold)">
        <div class="stat-num" style="color:var(--gold-dark)">{{ stats.total }}</div>
        <div class="stat-lbl">إجمالى الطلبات</div>
    </div>
    <div class="stat-card card anim-fade-up delay-2"
         style="border-right:3px solid #ff6644">
        <div class="stat-num" style="color:#ff6644">{{ stats.ongoing }}</div>
        <div class="stat-lbl">طلبات جارية</div>
    </div>
    <div class="stat-card card anim-fade-up delay-3"
         style="border-right:3px solid #00aa66">
        <div class="stat-num" style="color:#00aa66">{{ stats.delivered }}</div>
        <div class="stat-lbl">تم التسليم</div>
    </div>
</div>"""

# ============================================================
files['templates/partials/orders_table.html'] = """<div class="card" style="overflow:hidden;margin-bottom:var(--space-4)">

    <div style="padding:var(--space-4) var(--space-5);
                background:linear-gradient(135deg,#2d1a00,#1a0f00);
                display:flex;justify-content:space-between;align-items:center">
        <span style="font-size:var(--text-base);font-weight:var(--font-black);color:var(--gold-light)">
            📋 قائمة الطلبات
        </span>
        <span style="font-size:var(--text-xs);color:rgba(245,166,35,0.5)">
            {{ orders|length }} طلب
        </span>
    </div>

    <table class="data-table">
        <thead>
            <tr class="col-headers">
                <th class="col-th">رقم الطلب</th>
                <th class="col-th">العميل</th>
                <th class="col-th">المقاس</th>
                <th class="col-th">المساحة</th>
                <th class="col-th">الحالة</th>
                <th class="col-th">حذف</th>
            </tr>
        </thead>
        <tbody id="orders-table-body">
            {% for order in orders %}
                {% include "partials/order_row.html" %}
            {% else %}
                <tr>
                    <td colspan="6" style="text-align:center;padding:48px;color:var(--text-muted)">
                        <div style="font-size:40px;margin-bottom:10px">📋</div>
                        <div style="font-weight:var(--font-bold)">مفيش طلبات</div>
                        <div style="font-size:var(--text-xs);margin-top:4px">اضغط طلب جديد للبداية</div>
                    </td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</div>"""

# ============================================================
files['templates/partials/order_row.html'] = """<tr id="order-{{ order.id }}" class="data-row">

    <td>
        <div style="font-family:monospace;font-weight:var(--font-black);
                    font-size:var(--text-sm);color:var(--gold-dark)">
            {{ order.number }}
        </div>
        <div style="font-size:var(--text-xs);color:var(--text-muted);margin-top:2px">
            {{ order.created_at.strftime("%Y/%m/%d") }}
        </div>
        {% if order.delivery_date %}
        <div style="font-size:var(--text-xs);color:#ff8844;margin-top:2px">
            🚚 {{ order.delivery_date.strftime("%Y/%m/%d") }}
        </div>
        {% endif %}
    </td>

    <td>
        <div style="font-weight:var(--font-bold);color:var(--text-primary)">
            {{ order.customer_name }}
        </div>
        {% if order.customer_phone %}
        <div style="font-size:var(--text-xs);color:var(--text-muted);margin-top:2px">
            📱 {{ order.customer_phone }}
        </div>
        {% endif %}
    </td>

    <td style="color:var(--text-secondary);font-size:var(--text-sm)">
        {{ order.length }}م × {{ order.width }}م
    </td>

    <td style="font-weight:var(--font-bold);color:var(--gold-dark)">
        {{ order.area_display }} م²
    </td>

    <td>
        <form hx-post="/orders/{{ order.id }}/status"
              hx-target="#order-{{ order.id }}"
              hx-swap="outerHTML">
            {% set badge_class = "ongoing" if order.status == "جارى" else "ready" if order.status == "جاهز" else "done" %}
            <select name="new_status"
                    class="status-select badge badge-{{ badge_class }}"
                    onchange="this.form.requestSubmit()">
                <option value="جارى"        {% if order.status=="جارى" %}selected{% endif %}>جارى</option>
                <option value="جاهز"        {% if order.status=="جاهز" %}selected{% endif %}>جاهز</option>
                <option value="تم التسليم" {% if order.status=="تم التسليم" %}selected{% endif %}>تم التسليم</option>
            </select>
        </form>
    </td>

    <td>
        <button class="btn-danger"
                hx-delete="/orders/{{ order.id }}"
                hx-target="#order-{{ order.id }}"
                hx-swap="outerHTML"
                hx-confirm="هتحذف الطلب {{ order.number }}؟">
            🗑️
        </button>
    </td>
</tr>"""

# ============================================================
for path, content in files.items():
    full_path = os.path.join(base, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    lines = content.count('\n') + 1
    print(f"✅ {lines:3d} سطر ← {path}")

print("\n🎉 Templates كلها اتكتبت بنجاح")