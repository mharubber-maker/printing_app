from fastapi import APIRouter, Request, Form, Depends, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from config.database import get_db
from domain.orders.repository import OrderRepository
from domain.orders.service import OrderService
from domain.orders.schema import OrderCreate, OrderUpdateStatus
from domain.orders.model import Transaction, Order, OrderItem, User
from datetime import date, datetime
import hashlib
from typing import Optional, List

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="templates")

def get_service(db: Session = Depends(get_db)) -> OrderService: 
    return OrderService(OrderRepository(db))

# 1. مسارات الخزينة والماليات
@router.get("/finance/dashboard-data", response_class=HTMLResponse)
async def get_finance_dashboard(request: Request, db: Session = Depends(get_db)):
    transactions = db.query(Transaction).order_by(desc(Transaction.date)).all()
    total_in = sum(float(t.amount) for t in transactions if t.type == 'in')
    total_out = sum(float(t.amount) for t in transactions if t.type == 'out')
    net_profit = total_in - total_out
    
    items = db.query(OrderItem).all()
    total_rugs = len(items)
    total_area = sum(float(i.area or 0) for i in items if i.area)
    
    orders = db.query(Order).all()
    total_expected = sum(float(o.total_price or 0) for o in orders if o.total_price)
    
    # حساب المدفوع بناءً على جدول المدفوعات
    total_paid = 0
    for o in orders:
        total_paid += sum(float(p.amount) for p in o.payments)
        
    total_remaining = total_expected - total_paid
    
    return templates.TemplateResponse("partials/finance_data.html", {
        "request": request, "transactions": transactions,
        "total_in": f"{total_in:,.2f}", "total_out": f"{total_out:,.2f}", "net_profit": f"{net_profit:,.2f}",
        "total_rugs": total_rugs, "total_area": f"{total_area:,.2f}",
        "total_paid": f"{total_paid:,.2f}", "total_remaining": f"{total_remaining:,.2f}"
    })

# 2. مسارات التسويق
@router.get("/marketing/data", response_class=HTMLResponse)
async def get_marketing_data(request: Request, db: Session = Depends(get_db)):
    campaigns = db.query(Transaction).filter(Transaction.category == 'دعاية').order_by(desc(Transaction.date)).all()
    total_spent = sum(float(c.amount) for c in campaigns)
    return templates.TemplateResponse("partials/marketing_data.html", {"request": request, "campaigns": campaigns, "total_spent": f"{total_spent:,.2f}"})

@router.post("/marketing/add", response_class=HTMLResponse)
async def add_marketing_expense(request: Request, amount: float = Form(...), platform: str = Form(...), description: str = Form(...), db: Session = Depends(get_db)):
    full_desc = f"{platform} | {description}"
    new_expense = Transaction(amount=amount, type="out", category="دعاية", description=full_desc)
    db.add(new_expense)
    db.commit()
    campaigns = db.query(Transaction).filter(Transaction.category == 'دعاية').order_by(desc(Transaction.date)).all()
    total_spent = sum(float(c.amount) for c in campaigns)
    return templates.TemplateResponse("partials/marketing_data.html", {"request": request, "campaigns": campaigns, "total_spent": f"{total_spent:,.2f}"})

# 3. مسارات الإعدادات
@router.get("/settings/data", response_class=HTMLResponse)
async def get_settings_data(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(desc(User.created_at)).all()
    return templates.TemplateResponse("partials/settings_data.html", {"request": request, "users": users})

@router.post("/settings/users/add", response_class=HTMLResponse)
async def add_user(request: Request, full_name: str = Form(...), username: str = Form(...), password: str = Form(...), role: str = Form("موظف"), db: Session = Depends(get_db)):
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    new_user = User(full_name=full_name, username=username, password_hash=hashed_pw, role=role)
    try: 
        db.add(new_user)
        db.commit()
    except IntegrityError: 
        db.rollback()
    users = db.query(User).order_by(desc(User.created_at)).all()
    return templates.TemplateResponse("partials/settings_data.html", {"request": request, "users": users})


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
# 4. مسارات الطلبات (الأساسية)
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
    order = service.update_status(order_id, OrderUpdateStatus(new_status=new_status))
    return templates.TemplateResponse("partials/order_row.html", {"request": request, "order": order})

@router.delete("/{order_id}", response_class=HTMLResponse)
async def delete_order(order_id: str, service: OrderService = Depends(get_service)):
    service.delete_order(order_id)
    return HTMLResponse("")

@router.get("/{order_id}/pdf", response_class=HTMLResponse)
async def get_invoice_pdf(request: Request, order_id: str, service: OrderService = Depends(get_service)):
    order = service.repo.get_by_id(order_id)
    if not order: raise HTTPException(status_code=404, detail="الطلب غير موجود")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return templates.TemplateResponse("pdf/invoice.html", {"request": request, "order": order, "now": now})

# 👇 مسار العرض السريع للصور والتفاصيل 👇
@router.get("/{order_id}/details", response_class=HTMLResponse)
async def get_order_details(request: Request, order_id: str, service: OrderService = Depends(get_service)):
    order = service.repo.get_by_id(order_id)
    if not order: raise HTTPException(status_code=404, detail="الطلب غير موجود")
    
    # حساب المتبقي للعميل بأمان
    paid = sum(float(p.amount) for p in order.payments)
    remaining_amount = float(order.total_price or 0) - paid
    
    return templates.TemplateResponse("partials/order_details.html", {"request": request, "order": order, "remaining_amount": remaining_amount})


from fastapi.responses import FileResponse
import os

@router.get("/media")
async def serve_media(path: str):
    if os.path.exists(path):
        return FileResponse(path)
    raise HTTPException(status_code=404, detail="الملف غير موجود على السيرفر")
