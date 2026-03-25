from fastapi import APIRouter, Request, Form, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db
from domain.orders.repository import OrderRepository
from domain.orders.service import OrderService
from domain.orders.schema import OrderCreate, OrderUpdateStatus
from datetime import date, datetime
from typing import Optional, List

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="templates")

def get_service(db: Session = Depends(get_db)) -> OrderService: return OrderService(OrderRepository(db))

@router.post("/add", response_class=HTMLResponse)
async def add_order(
    request: Request,
    customer_name: str = Form(...), customer_phone: str = Form(""), customer_address: str = Form(""),
    lengths: List[float] = Form(...), widths: List[float] = Form(...), 
    prices_per_m2: List[float] = Form(...), factory_prices_per_m2: List[float] = Form(...),
    item_images: List[UploadFile] = File(default=[]), transfer_receipt: UploadFile = File(None),
    paid_amount: float = Form(0), payment_method: str = Form("كاش"), payment_ref: str = Form(""),
    shipping_company: str = Form(""), receipt_date: Optional[str] = Form(None), delivery_date: Optional[str] = Form(None),
    notes: str = Form(""), service: OrderService = Depends(get_service),
):
    data = OrderCreate(
        customer_name=customer_name, customer_phone=customer_phone, customer_address=customer_address,
        lengths=lengths, widths=widths, prices_per_m2=prices_per_m2, factory_prices_per_m2=factory_prices_per_m2,
        paid_amount=paid_amount, payment_method=payment_method, payment_ref=payment_ref,
        shipping_company=shipping_company, receipt_date=date.fromisoformat(receipt_date) if receipt_date else None,
        delivery_date=date.fromisoformat(delivery_date) if delivery_date else None, notes=notes
    )
    order = service.create_order(data, item_images, transfer_receipt)
    return templates.TemplateResponse("partials/order_row.html", {"request": request, "order": order})

@router.post("/{order_id}/status", response_class=HTMLResponse)
async def update_status(request: Request, order_id: str, new_status: str = Form(...), service: OrderService = Depends(get_service)):
    return templates.TemplateResponse("partials/order_row.html", {"request": request, "order": service.update_status(order_id, OrderUpdateStatus(new_status=new_status))})

@router.delete("/{order_id}", response_class=HTMLResponse)
async def delete_order(order_id: str, service: OrderService = Depends(get_service)):
    service.delete_order(order_id); return HTMLResponse("")

@router.get("/{order_id}/pdf", response_class=HTMLResponse)
async def get_invoice_pdf(request: Request, order_id: str, service: OrderService = Depends(get_service)):
    order = service.repo.get_by_id(order_id)
    if not order: raise HTTPException(status_code=404, detail="الطلب غير موجود")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return templates.TemplateResponse("pdf/invoice.html", {"request": request, "order": order, "now": now})

# 👇 مسار لوحة القيادة المالية (HTMX Endpoint) 👇
@router.get("/finance/dashboard-data", response_class=HTMLResponse)
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

@router.get("/marketing/data", response_class=HTMLResponse)
async def get_marketing_data(request: Request, db: Session = Depends(get_db)):
    from domain.orders.model import Transaction
    from sqlalchemy import desc
    # جلب معاملات الدعاية فقط
    campaigns = db.query(Transaction).filter(Transaction.category == 'دعاية').order_by(desc(Transaction.date)).all()
    total_spent = sum(float(c.amount) for c in campaigns)
    
    return templates.TemplateResponse("partials/marketing_data.html", {
        "request": request, 
        "campaigns": campaigns, 
        "total_spent": f"{total_spent:,.2f}"
    })

# 👇 مسار إضافة مصروف إعلاني جديد 👇
@router.post("/marketing/add", response_class=HTMLResponse)
async def add_marketing_expense(
    request: Request, 
    amount: float = Form(...), 
    platform: str = Form(...), 
    description: str = Form(...), 
    db: Session = Depends(get_db)
):
    from domain.orders.model import Transaction
    from sqlalchemy import desc
    
    # حفظ المصروف في دفتر الأستاذ
    full_desc = f"{platform} | {description}"
    new_expense = Transaction(amount=amount, type="out", category="دعاية", description=full_desc)
    db.add(new_expense)
    db.commit()
    
    # إعادة جلب البيانات لتحديث الشاشة
    campaigns = db.query(Transaction).filter(Transaction.category == 'دعاية').order_by(desc(Transaction.date)).all()
    total_spent = sum(float(c.amount) for c in campaigns)
    
    return templates.TemplateResponse("partials/marketing_data.html", {
        "request": request, 
        "campaigns": campaigns, 
        "total_spent": f"{total_spent:,.2f}"
    })

# 👇 مسار جلب لوحة الإعدادات 👇
@router.get("/settings/data", response_class=HTMLResponse)
async def get_settings_data(request: Request, db: Session = Depends(get_db)):
    from domain.orders.model import User
    from sqlalchemy import desc
    # جلب قائمة الموظفين
    users = db.query(User).order_by(desc(User.created_at)).all()
    
    return templates.TemplateResponse("partials/settings_data.html", {
        "request": request, 
        "users": users
    })

# 👇 مسار إضافة موظف جديد 👇
@router.post("/settings/users/add", response_class=HTMLResponse)
async def add_user(
    request: Request, 
    full_name: str = Form(...), 
    username: str = Form(...), 
    password: str = Form(...), 
    role: str = Form("موظف"),
    db: Session = Depends(get_db)
):
    from domain.orders.model import User
    from sqlalchemy import desc
    from sqlalchemy.exc import IntegrityError
    import hashlib
    
    # تشفير كلمة المرور (Security Best Practice)
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    
    new_user = User(full_name=full_name, username=username, password_hash=hashed_pw, role=role)
    
    try:
        db.add(new_user)
        db.commit()
    except IntegrityError:
        db.rollback() # حماية في حال كان اسم المستخدم موجود مسبقاً
        
    # إعادة جلب قائمة الموظفين لتحديث الشاشة
    users = db.query(User).order_by(desc(User.created_at)).all()
    
    return templates.TemplateResponse("partials/settings_data.html", {
        "request": request, 
        "users": users
    })

# 👇 مسار العرض السريع (Quick View) 👇
@router.get("/{order_id}/details", response_class=HTMLResponse)
async def get_order_details(request: Request, order_id: str, service: OrderService = Depends(get_service)):
    order = service.repo.get_by_id(order_id)
    if not order: raise HTTPException(status_code=404, detail="الطلب غير موجود")
    return templates.TemplateResponse("partials/order_details.html", {"request": request, "order": order})
