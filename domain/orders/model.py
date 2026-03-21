from sqlalchemy import Column, Integer, String, Numeric, DateTime, Date, Text
from datetime import datetime
from config.database import Base
from config.constants import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    id            = Column(Integer, primary_key=True, index=True)
    number        = Column(String(20), unique=True, index=True, nullable=False)
    customer_name = Column(String(100), nullable=False)
    customer_phone= Column(String(20))
    length        = Column(Numeric(8, 2), nullable=False)
    width         = Column(Numeric(8, 2), nullable=False)
    area          = Column(Numeric(8, 2))
    status        = Column(String(20), default=OrderStatus.PENDING)
    notes         = Column(Text)
    delivery_date = Column(Date)
    image_path    = Column(String(500))
    created_at    = Column(DateTime, default=datetime.utcnow)
    updated_at    = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def area_display(self) -> str:
        if not self.length or not self.width:
            return "—"
        area = round(float(self.length) * float(self.width), 2)
        return str(int(area)) if area == int(area) else str(area)

    @property
    def status_color(self) -> str:
        from config.constants import OrderStatus
        return OrderStatus.COLORS.get(self.status, "gray")

    def __repr__(self):
        return f"<Order {self.number} - {self.customer_name}>"
