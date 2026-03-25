import os

with open("domain/orders/router.py", "r", encoding="utf-8") as f:
    content = f.read()

if '@router.get("/shipping/data"' not in content:
    shipping_route = """
# 👇 مسارات قسم الشحن 👇
@router.get("/shipping/data", response_class=HTMLResponse)
async def get_shipping_data(request: Request, db: Session = Depends(get_db)):
    from domain.orders.model import Order
    # جلب الطلبات الجاهزة للشحن فقط
    ready_orders = db.query(Order).filter(Order.status == 'جاهز').all()
    
    # تجميع الطلبات حسب شركة الشحن (Grouping)
    companies = {}
    for o in ready_orders:
        comp = o.shipping_company.strip() if o.shipping_company else "مناديب حرة (بدون شركة)"
        if comp not in companies:
            companies[comp] = []
        companies[comp].append(o)
        
    return templates.TemplateResponse("partials/shipping_data.html", {
        "request": request, 
        "companies": companies
    })

@router.get("/shipping", response_class=HTMLResponse)
async def shipping_page(request: Request):
    return templates.TemplateResponse("pages/shipping.html", {"request": request})
"""
    # حقن المسار قبل دوال الطلبات الأساسية
    insert_pos = content.find('# 4. مسارات الطلبات (الأساسية)')
    if insert_pos != -1:
        content = content[:insert_pos] + shipping_route + content[insert_pos:]
        with open("domain/orders/router.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ تم إضافة مسارات الشحن للـ Backend!")
