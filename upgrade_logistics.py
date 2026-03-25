import re
import os

# 1. تحديث الباك-إند لفصل نظام التعيين
router_path = "domain/orders/router.py"
with open(router_path, "r", encoding="utf-8") as f:
    code = f.read()

# مسح دالة get_shipping_data القديمة ووضع النظام الجديد
old_func_pattern = r'@router\.get\("/shipping/data".*?return templates\.TemplateResponse\("partials/shipping_data\.html"[^\)]+\)'
new_logic = """@router.get("/shipping/data", response_class=HTMLResponse)
async def get_shipping_data(request: Request, db: Session = Depends(get_db)):
    from domain.orders.model import Order
    ready_orders = db.query(Order).filter(Order.status == 'جاهز').all()
    companies = {}
    for o in ready_orders:
        comp = o.shipping_company.strip() if o.shipping_company else ""
        if comp not in companies: companies[comp] = []
        companies[comp].append(o)
    return templates.TemplateResponse("partials/shipping_data.html", {"request": request, "companies": companies})

@router.post("/{order_id}/shipping", response_class=HTMLResponse)
async def update_shipping_company(request: Request, order_id: str, shipping_company: str = Form(""), db: Session = Depends(get_db)):
    from domain.orders.model import Order
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        order.shipping_company = shipping_company
        db.commit()
    
    # إعادة تحميل شاشة الشحن بعد التحديث
    ready_orders = db.query(Order).filter(Order.status == 'جاهز').all()
    companies = {}
    for o in ready_orders:
        comp = o.shipping_company.strip() if o.shipping_company else ""
        if comp not in companies: companies[comp] = []
        companies[comp].append(o)
    return templates.TemplateResponse("partials/shipping_data.html", {"request": request, "companies": companies})"""

if re.search(old_func_pattern, code, re.DOTALL):
    code = re.sub(old_func_pattern, new_logic, code, flags=re.DOTALL)
else:
    # في حالة عدم العثور عليها، يتم الإضافة في النهاية
    code += "\n" + new_logic

with open(router_path, "w", encoding="utf-8") as f:
    f.write(code)

# 2. إخفاء حقل الشحن من نافذة إضافة طلب بأمان تام
modal_path = "templates/components/modal.html"
if os.path.exists(modal_path):
    with open(modal_path, "a", encoding="utf-8") as f:
        # حقن سكريبت صغير يمسح الحقل من الواجهة بمجرد فتحها
        f.write("\n<script>document.querySelectorAll('[name=\"shipping_company\"]').forEach(el => { if(el.closest('div')) el.closest('div').style.display = 'none'; });</script>")

print("✅ Backend updated successfully!")
