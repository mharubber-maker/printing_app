from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from config.database import get_db, engine, Base
from config.settings import settings
from domain.orders.repository import OrderRepository
from domain.orders.model import Order, Customer, OrderItem, OrderImage, Payment, ProductionLog, User
from domain.orders.router import router as orders_router
import uvicorn
import io
from fastapi.responses import StreamingResponse
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from datetime import datetime

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Routers
app.include_router(orders_router)


# ========== الصفحة الرئيسية ==========
@app.get("/", response_class=HTMLResponse)
async def dashboard(
    request: Request,
    search:  str = "",
    status:  str = "",
    db:      Session = Depends(get_db),
):
    repo   = OrderRepository(db)
    orders = repo.get_all(search=search, status=status)
    stats  = repo.get_stats()

    return templates.TemplateResponse("pages/dashboard.html", {
        "request": request,
        "orders":  orders,
        "stats":   stats,
        "search":  search,
        "status":  status,
    })


# ========== الإحصائيات (HTMX) ==========
@app.get("/stats", response_class=HTMLResponse)
async def get_stats(
    request: Request,
    db:      Session = Depends(get_db),
):
    stats = OrderRepository(db).get_stats()
    return templates.TemplateResponse("partials/stats.html", {
        "request": request,
        "stats":   stats,
    })


@app.get("/orders/{order_id}/pdf")
async def generate_pdf(
    order_id: str,
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return HTMLResponse("الطلب مش موجود", status_code=404)

    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("pdf/invoice.html")
    html_content = template.render(
        order=order,
        now=datetime.now().strftime("%d/%m/%Y %H:%M")
    )

    pdf_bytes = HTML(string=html_content).write_pdf()

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={order.number}.pdf"}
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=7860,
        reload=settings.DEBUG,
    )
