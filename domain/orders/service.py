from domain.orders.model import Order, Customer, OrderItem, OrderImage, Payment, Transaction
from domain.orders.schema import OrderCreate, OrderUpdateStatus
from domain.orders.repository import OrderRepository
from config.constants import OrderStatus
import os, shutil, uuid

class OrderService:
    def __init__(self, repo: OrderRepository): self.repo = repo
    def get_all(self, search: str = "", status: str = "") -> list[Order]: return self.repo.get_all(search=search, status=status)
    def get_stats(self) -> dict: return self.repo.get_stats()

    def create_order(self, data: OrderCreate, item_images=None, transfer_receipt=None) -> Order:
        number = self._generate_number()
        customer = Customer(name=data.customer_name, phone=data.customer_phone, address=data.customer_address, notes=data.notes)
        order = Order(number=number, notes=data.notes, status=OrderStatus.PENDING, customer=customer, shipping_company=data.shipping_company, receipt_date=data.receipt_date, delivery_date=data.delivery_date)
        
        total_order_price = 0
        total_factory_cost = 0 # لحساب إجمالي تكلفة المصنع
        
        for i in range(len(data.lengths)):
            l = data.lengths[i]; w = data.widths[i]; p = data.prices_per_m2[i]; fp = data.factory_prices_per_m2[i]
            img = item_images[i] if item_images and i < len(item_images) else None
            area = round(l * w, 2)
            item_total = round(area * p, 2)
            factory_total = round(area * fp, 2)
            
            total_order_price += item_total
            total_factory_cost += factory_total
            
            img_path = self._save_image(img) if img and img.filename else None
            order.items.append(OrderItem(length=l, width=w, area=area, price_per_m2=p, factory_price_per_m2=fp, total=item_total, image_path=img_path, description="طباعة"))

        order.total_price = total_order_price

        # تسجيل الدفعة وإيراد الخزينة
        if data.paid_amount > 0:
            db_method = "تحويل" if data.payment_method in ["فودافون كاش", "انستا باي", "تحويل بنكي"] else "كاش"
            db_notes = f"تم الدفع عبر: {data.payment_method} | رقم العملية: {data.payment_ref}" if data.payment_ref else f"تم الدفع عبر: {data.payment_method}"
            order.payments.append(Payment(amount=data.paid_amount, payment_method=db_method, notes=db_notes))
            
            if transfer_receipt and transfer_receipt.filename:
                order.images.append(OrderImage(image_path=self._save_image(transfer_receipt), caption="إيصال دفع"))
            
            # 👇 تسجيل معاملة (إيراد) في دفتر الأستاذ 👇
            order.transactions.append(Transaction(amount=data.paid_amount, type="in", category="مبيعات", description=f"دفعة مقدمة من العميل لطلب {number}"))

        # 👇 تسجيل معاملة (مصروف) للمصنع في دفتر الأستاذ 👇
        if total_factory_cost > 0:
            order.transactions.append(Transaction(amount=total_factory_cost, type="out", category="مصنع", description=f"تكلفة إنتاج المصنع للطلب {number}"))

        return self.repo.create(order)

    def update_status(self, order_id: str, data: OrderUpdateStatus) -> Order:
        order = self.repo.get_by_id(order_id); if not order: raise ValueError("Order not found")
        order.status = data.new_status; return self.repo.update(order)

    def delete_order(self, order_id: str) -> bool:
        order = self.repo.get_by_id(order_id); if not order: raise ValueError("Order not found")
        if order.items:
            for item in order.items:
                if item.image_path and os.path.exists(item.image_path): os.remove(item.image_path)
        if order.images:
            for img in order.images:
                if img.image_path and os.path.exists(img.image_path): os.remove(img.image_path)
        return self.repo.delete(order)

    def _generate_number(self) -> str: return f"ORD-{self.repo.count() + 1:03d}"
    def _save_image(self, image) -> str:
        d = "static/uploads"; os.makedirs(d, exist_ok=True); p = f"{d}/{uuid.uuid4()}{os.path.splitext(image.filename)[1]}"
        with open(p, "wb") as f: shutil.copyfileobj(image.file, f); return p
