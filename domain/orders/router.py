from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db
from domain.orders.repository import OrderRepository
from domain.orders.service import OrderService
from domain.orders.schema import OrderCreate, OrderUpdateStatus
from datetime import date
from typing import Optional, List

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="templates")

def get_service(db: Session = Depends(get_db)) -> OrderService: return OrderService(OrderRepository(db))

@router.post("/add", response_class=HTMLResponse)
async def add_order(
    request:        Request,
    customer_name:  str            = Form(...),
    customer_phone: str            = Form(""),
    lengths:        List[float]    = Form(...),
    widths:         List[float]    = Form(...),
    prices_per_m2:  List[float]    = Form(...), # استقبال قائمة الأسعار
    paid_amount:    float          = Form(0),
    payment_method: str            = Form("كاش"),
    payment_ref:    str            = Form(""),
    notes:          str            = Form(""),
    delivery_date:  Optional[str]  = Form(None),
    image:          UploadFile     = File(None),
    service:        OrderService   = Depends(get_service),
):
    data = OrderCreate(
        customer_name=customer_name, customer_phone=customer_phone,
        lengths=lengths, widths=widths, prices_per_m2=prices_per_m2,
        paid_amount=paid_amount, payment_method=payment_method, payment_ref=payment_ref,
        notes=notes, delivery_date=date.fromisoformat(delivery_date) if delivery_date else None,
    )
    order = service.create_order(data, image)
    return templates.TemplateResponse("partials/order_row.html", {"request": request, "order": order})

@router.post("/{order_id}/status", response_class=HTMLResponse)
async def update_status(request: Request, order_id: str, new_status: str = Form(...), service: OrderService = Depends(get_service)):
    return templates.TemplateResponse("partials/order_row.html", {"request": request, "order": service.update_status(order_id, OrderUpdateStatus(new_status=new_status))})

@router.delete("/{order_id}", response_class=HTMLResponse)
async def delete_order(order_id: str, service: OrderService = Depends(get_service)):
    service.delete_order(order_id); return HTMLResponse("")
