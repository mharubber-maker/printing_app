import uuid
from sqlalchemy import Column, String, Numeric, DateTime, Date, Text, ForeignKey, Boolean, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base
from config.constants import OrderStatus

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="موظف")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    orders_created = relationship("Order", foreign_keys="Order.created_by", back_populates="creator")
    payments_received = relationship("Payment", foreign_keys="Payment.received_by", back_populates="receiver")

class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    address = Column(Text) # العنوان موجود بالفعل
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (CheckConstraint("status IN ('جارى', 'جاهز', 'تم التسليم', 'ملغى')", name="valid_status"),)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    number = Column(String(20), unique=True, nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default=OrderStatus.PENDING)
    total_price = Column(Numeric(10, 2), default=0)
    
    # 👇 الحقول الجديدة الخاصة بالشحن والمواعيد
    shipping_company = Column(String(100), nullable=True)
    receipt_date = Column(Date, nullable=True) 
    delivery_date = Column(Date, nullable=True)
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    customer = relationship("Customer", back_populates="orders")
    creator = relationship("User", foreign_keys=[created_by], back_populates="orders_created")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    images = relationship("OrderImage", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")
    logs = relationship("ProductionLog", back_populates="order", cascade="all, delete-orphan")

    @property
    def paid_amount(self): return sum(float(p.amount or 0) for p in self.payments)
    @property
    def remaining_amount(self): return float(self.total_price or 0) - self.paid_amount

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    description = Column(Text)
    length = Column(Numeric(8, 2), nullable=False)
    width = Column(Numeric(8, 2), nullable=False)
    area = Column(Numeric(8, 2))
    price_per_m2 = Column(Numeric(8, 2), default=0)
    total = Column(Numeric(10, 2), default=0)
    
    # 👇 الحقل الجديد للصورة المستقلة لكل سجادة
    image_path = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    order = relationship("Order", back_populates="items")

class OrderImage(Base):
    __tablename__ = "order_images"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    image_path = Column(Text, nullable=False)
    caption = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    order = relationship("Order", back_populates="images")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    received_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String(20), default="كاش")
    notes = Column(Text)
    paid_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
    order = relationship("Order", back_populates="payments")
    receiver = relationship("User", foreign_keys=[received_by], back_populates="payments_received")

class ProductionLog(Base):
    __tablename__ = "production_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    stage = Column(String(50), nullable=False)
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    order = relationship("Order", back_populates="logs")
