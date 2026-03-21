from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.database import get_db
from domain.orders.repository import OrderRepository
from domain.orders.service import OrderService
from domain.orders.schema import OrderCreate, OrderUpdateStatus
from datetime import date
from typing import Optional

router = APIRouter(prefix="/orders", tags=["orders"])
templates = Jinja2Templates(directory="templates")


def get_service(db: Session = Depends(get_db)) -> OrderService:
    return OrderService(OrderRepository(db))


@router.post("/add", response_class=HTMLResponse)
async def add_order(
    request:       Request,
    customer_name: str            = Form(...),
    customer_phone:str            = Form(""),
    length:        float          = Form(...),
    width:         float          = Form(...),
    notes:         str            = Form(""),
    delivery_date: Optional[str]  = Form(None),
    image:         UploadFile     = File(None),
    service:       OrderService   = Depends(get_service),
):
    data = OrderCreate(
        customer_name=customer_name,
        customer_phone=customer_phone,
        length=length,
        width=width,
        notes=notes,
        delivery_date=date.fromisoformat(delivery_date) if delivery_date else None,
    )
    order = service.create_order(data, image)
    return templates.TemplateResponse(
        "partials/order_row.html",
        {"request": request, "order": order}
    )


@router.post("/{order_id}/status", response_class=HTMLResponse)
async def update_status(
    request:    Request,
    order_id:   int,
    new_status: str           = Form(...),
    service:    OrderService  = Depends(get_service),
):
    data  = OrderUpdateStatus(new_status=new_status)
    order = service.update_status(order_id, data)
    return templates.TemplateResponse(
        "partials/order_row.html",
        {"request": request, "order": order}
    )


@router.delete("/{order_id}", response_class=HTMLResponse)
async def delete_order(
    order_id: int,
    service:  OrderService = Depends(get_service),
):
    service.delete_order(order_id)
    return HTMLResponse("")
