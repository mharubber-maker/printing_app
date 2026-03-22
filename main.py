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
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return HTMLResponse("الطلب مش موجود", status_code=404)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)

    styles = getSampleStyleSheet()
    gold   = colors.HexColor("#f5a623")
    dark   = colors.HexColor("#1a0f00")
    white  = colors.white

    # styles
    title_style = ParagraphStyle("title", fontSize=18, textColor=gold,
                                 alignment=TA_RIGHT, fontName="Helvetica-Bold")
    header_style = ParagraphStyle("header", fontSize=12, textColor=white,
                                  alignment=TA_RIGHT, fontName="Helvetica-Bold")
    normal_style = ParagraphStyle("normal", fontSize=11, textColor=dark,
                                  alignment=TA_RIGHT)
    label_style  = ParagraphStyle("label", fontSize=9, textColor=colors.grey,
                                  alignment=TA_RIGHT)

    story = []

    # Header box
    header_data = [[
        Paragraph(f"Invoice | {order.number}", ParagraphStyle("inv", fontSize=14,
                  textColor=gold, alignment=TA_LEFT, fontName="Helvetica-Bold")),
        Paragraph("Printing & Colors House", header_style)
    ]]
    header_table = Table(header_data, colWidths=[8*cm, 9*cm])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), dark),
        ("PADDING",    (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.4*cm))

    # Rainbow line
    rainbow = Table([[""]], colWidths=[17*cm])
    rainbow.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), gold),
        ("ROWHEIGHT",  (0,0), (-1,-1), 4),
    ]))
    story.append(rainbow)
    story.append(Spacer(1, 0.6*cm))

    # Customer & Order info
    customer_name  = order.customer.name  if order.customer else "—"
    customer_phone = order.customer.phone if order.customer and order.customer.phone else "—"
    order_date     = order.created_at.strftime("%d/%m/%Y") if order.created_at else "—"
    delivery_date  = order.delivery_date.strftime("%d/%m/%Y") if order.delivery_date else "—"

    info_data = [
        [Paragraph("Customer", label_style),  Paragraph("Order Date", label_style)],
        [Paragraph(customer_name, normal_style), Paragraph(order_date, normal_style)],
        [Paragraph(customer_phone, label_style), Paragraph(f"Delivery: {delivery_date}", label_style)],
    ]
    info_table = Table(info_data, colWidths=[8.5*cm, 8.5*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), colors.HexColor("#faf6f0")),
        ("BOX",         (0,0), (-1,-1), 1, colors.HexColor("#e8d8b8")),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#f0e8d8")),
        ("PADDING",     (0,0), (-1,-1), 8),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.6*cm))

    # Items table
    table_data = [["Total", "Price/m2", "Area m2", "Width", "Length", "Description", "#"]]
    if order.items:
        for i, item in enumerate(order.items, 1):
            table_data.append([
                str(item.total or "—"),
                str(item.price_per_m2 or "—"),
                str(item.area or "—"),
                str(item.width),
                str(item.length),
                item.description or "—",
                str(i),
            ])
    else:
        table_data.append([
            str(order.total_price), "—",
            order.area_display, "—", "—", order.number, "1"
        ])

    items_table = Table(table_data,
                        colWidths=[2.5*cm, 2.5*cm, 2.5*cm, 2*cm, 2*cm, 3.5*cm, 1*cm])
    items_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0), dark),
        ("TEXTCOLOR",   (0,0), (-1,0), gold),
        ("FONTNAME",    (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fdf8f0")]),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#e8d8b8")),
        ("PADDING",     (0,0), (-1,-1), 6),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.6*cm))

    # Totals
    paid      = order.paid_amount
    remaining = order.remaining_amount
    totals_data = [
        ["Total",     f"{order.total_price} EGP"],
        ["Paid",      f"{paid:.2f} EGP"],
        ["Remaining", f"{remaining:.2f} EGP"],
    ]
    totals_table = Table(totals_data, colWidths=[4*cm, 4*cm])
    totals_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), colors.HexColor("#faf6f0")),
        ("BOX",         (0,0), (-1,-1), 1, colors.HexColor("#e8d8b8")),
        ("FONTNAME",    (0,2), (-1,2), "Helvetica-Bold"),
        ("TEXTCOLOR",   (0,2), (-1,2), gold),
        ("FONTSIZE",    (0,0), (-1,-1), 10),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#f0e8d8")),
        ("PADDING",     (0,0), (-1,-1), 8),
    ]))
    story.append(totals_table)
    story.append(Spacer(1, 0.4*cm))

    # Notes
    if order.notes:
        story.append(Paragraph(f"Notes: {order.notes}", normal_style))
        story.append(Spacer(1, 0.3*cm))

    # Footer
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    story.append(Paragraph(f"Generated: {now} | Printing & Colors House",
                           ParagraphStyle("footer", fontSize=8,
                                         textColor=colors.grey, alignment=TA_CENTER)))

    doc.build(story)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
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
