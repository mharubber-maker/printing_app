import os

# 1. تحديث قالب الخزينة (HTML)
html_content = """<div style="animation: fadeIn 0.5s;">
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px;">
        <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 16px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 8px;">🧶</div>
            <div style="color: var(--text-muted); font-size: 11px; font-weight: bold;">إجمالي عدد السجاد</div>
            <div style="color: var(--text-primary); font-size: 20px; font-weight: 900; margin-top: 4px;">{{ total_rugs }} <span style="font-size: 12px; font-weight: normal;">قطعة</span></div>
        </div>
        
        <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 10px; padding: 16px; text-align: center;">
            <div style="font-size: 24px; margin-bottom: 8px;">📏</div>
            <div style="color: var(--text-muted); font-size: 11px; font-weight: bold;">مساحة الأمتار العامة</div>
            <div style="color: var(--text-primary); font-size: 20px; font-weight: 900; margin-top: 4px;">{{ total_area }} <span style="font-size: 12px; font-weight: normal;">م²</span></div>
        </div>
        
        <div style="background: var(--bg-card); border: 1px solid #10b981; border-radius: 10px; padding: 16px; text-align: center; box-shadow: 0 4px 10px rgba(16,185,129,0.05);">
            <div style="font-size: 24px; margin-bottom: 8px;">💵</div>
            <div style="color: #10b981; font-size: 11px; font-weight: bold;">العربون (تم تحصيله)</div>
            <div style="color: white; font-size: 20px; font-weight: 900; margin-top: 4px;">{{ total_paid }} <span style="font-size: 12px; font-weight: normal; color: #a0a0a0;">ج.م</span></div>
        </div>
        
        <div style="background: var(--bg-card); border: 1px solid #ef4444; border-radius: 10px; padding: 16px; text-align: center; box-shadow: 0 4px 10px rgba(239,68,68,0.05);">
            <div style="font-size: 24px; margin-bottom: 8px;">⏳</div>
            <div style="color: #ef4444; font-size: 11px; font-weight: bold;">الباقي لم يُحصّل</div>
            <div style="color: white; font-size: 20px; font-weight: 900; margin-top: 4px;">{{ total_remaining }} <span style="font-size: 12px; font-weight: normal; color: #a0a0a0;">ج.م</span></div>
        </div>
    </div>

    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px;">
        <div style="background: linear-gradient(135deg, #0f2a1d, #05120c); border: 1px solid #10b981; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.1);">
            <div style="color: #10b981; font-size: 12px; font-weight: bold; margin-bottom: 8px;">📈 إجمالي إيرادات الخزينة</div>
            <div style="color: white; font-size: 28px; font-weight: 900;">{{ total_in }} <span style="font-size: 14px; color: #a0a0a0;">ج.م</span></div>
        </div>

        <div style="background: linear-gradient(135deg, #3a1010, #1a0505); border: 1px solid #ef4444; border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);">
            <div style="color: #ef4444; font-size: 12px; font-weight: bold; margin-bottom: 8px;">📉 إجمالي المصروفات (المصنع)</div>
            <div style="color: white; font-size: 28px; font-weight: 900;">{{ total_out }} <span style="font-size: 14px; color: #a0a0a0;">ج.م</span></div>
        </div>

        <div style="background: linear-gradient(135deg, #2d1a00, #1a0f00); border: 1px solid var(--gold-dark); border-radius: 12px; padding: 20px; box-shadow: 0 4px 15px rgba(245, 166, 35, 0.15);">
            <div style="color: var(--gold-dark); font-size: 12px; font-weight: bold; margin-bottom: 8px;">💰 صافي الربح الحقيقي</div>
            <div style="color: #ffd700; font-size: 28px; font-weight: 900;">{{ net_profit }} <span style="font-size: 14px; color: rgba(245,166,35,0.5);">ج.م</span></div>
        </div>
    </div>

    <div style="background:var(--bg-card); border-radius:12px; overflow:hidden; border:1px solid var(--border-color);">
        <div style="padding:16px 20px; background:var(--bg-table-head); display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:15px; font-weight:bold; color:var(--gold-dark)">🧾 دفتر الأستاذ العام (حركة الخزينة)</span>
            <span style="font-size:11px; color:var(--text-muted);">أحدث المعاملات</span>
        </div>
        <table style="width:100%; border-collapse:collapse; text-align:right;">
            <thead>
                <tr style="border-bottom:1px solid var(--border-color);">
                    <th style="padding:12px 16px; font-size:11px; color:var(--text-muted);">التاريخ</th>
                    <th style="padding:12px 16px; font-size:11px; color:var(--text-muted);">التصنيف</th>
                    <th style="padding:12px 16px; font-size:11px; color:var(--text-muted);">البيان (الوصف)</th>
                    <th style="padding:12px 16px; font-size:11px; color:var(--text-muted);">المبلغ</th>
                </tr>
            </thead>
            <tbody>
                {% for t in transactions %}
                <tr style="border-bottom:1px solid rgba(255,255,255,0.05); transition: 0.2s;" onmouseover="this.style.backgroundColor='var(--bg-table-hover)'" onmouseout="this.style.backgroundColor='transparent'">
                    <td style="padding:12px 16px; font-size:12px; color:var(--text-primary);">{{ t.date.strftime('%Y-%m-%d %H:%M') }}</td>
                    <td style="padding:12px 16px;">
                        <span style="font-size:11px; padding:3px 8px; border-radius:4px; font-weight:bold; 
                            {% if t.category == 'مبيعات' %}background:rgba(16,185,129,0.1); color:#10b981;
                            {% elif t.category == 'مصنع' %}background:rgba(239,68,68,0.1); color:#ef4444;
                            {% else %}background:rgba(245,166,35,0.1); color:var(--gold-dark);{% endif %}">
                            {{ t.category }}
                        </span>
                    </td>
                    <td style="padding:12px 16px; font-size:12px; color:var(--text-muted);">{{ t.description }}</td>
                    <td style="padding:12px 16px; font-weight:bold; font-size:13px; {% if t.type == 'in' %}color:#10b981;{% else %}color:#ef4444;{% endif %}">
                        {% if t.type == 'in' %}+{% else %}-{% endif %} {{ t.amount }} ج
                    </td>
                </tr>
                {% else %}
                <tr><td colspan="4" style="text-align:center; padding:40px; color:var(--text-muted);">لم يتم تسجيل أي معاملات مالية حتى الآن.</td></tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>"""

with open("templates/partials/finance_data.html", "w", encoding="utf-8") as f:
    f.write(html_content)

# 2. تحديث الموجه (Router) وإضافة العمليات الحسابية
with open("domain/orders/router.py", "r", encoding="utf-8") as f:
    content = f.read()

start_idx = content.find('@router.get("/finance/dashboard-data"')
end_idx = content.find('@router.get("/marketing/data"', start_idx)

new_func = """@router.get("/finance/dashboard-data", response_class=HTMLResponse)
async def get_finance_dashboard(request: Request, db: Session = Depends(get_db)):
    from domain.orders.model import Transaction, Order, OrderItem
    from sqlalchemy import desc
    
    # حسابات دفتر الأستاذ
    transactions = db.query(Transaction).order_by(desc(Transaction.date)).all()
    total_in = sum(float(t.amount) for t in transactions if t.type == 'in')
    total_out = sum(float(t.amount) for t in transactions if t.type == 'out')
    net_profit = total_in - total_out
    
    # حسابات الإنتاج (السجاد والأمتار)
    items = db.query(OrderItem).all()
    total_rugs = len(items)
    total_area = sum(float(i.area or 0) for i in items if i.area)
    
    # حسابات التحصيل (المدفوع والمتبقي)
    orders = db.query(Order).all()
    total_expected = sum(float(o.total_price or 0) for o in orders if o.total_price)
    total_paid = sum(float(o.paid_amount or 0) for o in orders)
    total_remaining = total_expected - total_paid
    
    return templates.TemplateResponse("partials/finance_data.html", {
        "request": request,
        "transactions": transactions,
        "total_in": f"{total_in:,.2f}",
        "total_out": f"{total_out:,.2f}",
        "net_profit": f"{net_profit:,.2f}",
        "total_rugs": total_rugs,
        "total_area": f"{total_area:,.2f}",
        "total_paid": f"{total_paid:,.2f}",
        "total_remaining": f"{total_remaining:,.2f}"
    })

"""

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + new_func + content[end_idx:]
    with open("domain/orders/router.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("✅ Backend updated successfully!")
