from domain.orders.model import Order, Customer, OrderItem, OrderImage, Payment
from domain.orders.schema import OrderCreate, OrderUpdateStatus
from domain.orders.repository import OrderRepository
from config.constants import OrderStatus
import os, shutil, uuid

class OrderService:
    def __init__(self, repo: OrderRepository): self.repo = repo
    def get_all(self, search: str = "", status: str = "") -> list[Order]: return self.repo.get_all(search=search, status=status)
    def get_stats(self) -> dict: return self.repo.get_stats()

    def create_order(self, data: OrderCreate, item_images=None) -> Order:
        number = self._generate_number()
        # إضافة العنوان للعميل
        customer = Customer(name=data.customer_name, phone=data.customer_phone, address=data.customer_address, notes=data.notes)
        order = Order(
            number=number, notes=data.notes, status=OrderStatus.PENDING, customer=customer,
            shipping_company=data.shipping_company, receipt_date=data.receipt_date, delivery_date=data.delivery_date
        )
        
        total_order_price = 0
        # معالجة كل سجادة على حدة مع صورتها
        for i in range(len(data.lengths)):
            l = data.lengths[i]
            w = data.widths[i]
            p = data.prices_per_m2[i]
            img = item_images[i] if item_images and i < len(item_images) else None
            
            area = round(l * w, 2)
            item_total = round(area * p, 2)
            total_order_price += item_total
            
            # حفظ صورة السجادة إذا وجدت
            img_path = self._save_image(img) if img and img.filename else None
            item = OrderItem(length=l, width=w, area=area, price_per_m2=p, total=item_total, image_path=img_path, description="طباعة")
            order.items.append(item)

        order.total_price = total_order_price

        if data.paid_amount > 0:
            db_method = "تحويل" if data.payment_method in ["فودافون كاش", "انستا باي", "تحويل بنكي"] else "كاش"
            db_notes = f"تم الدفع عبر: {data.payment_method}"
            if data.payment_ref: db_notes += f" | رقم العملية: {data.payment_ref}"
            order.payments.append(Payment(amount=data.paid_amount, payment_method=db_method, notes=db_notes))

        return self.repo.create(order)

    def update_status(self, order_id: str, data: OrderUpdateStatus) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order: raise ValueError("Order not found")
        order.status = data.new_status
        return self.repo.update(order)

    def delete_order(self, order_id: str) -> bool:
        order = self.repo.get_by_id(order_id)
        if not order: raise ValueError("Order not found")
        if order.items:
            for item in order.items:
                if item.image_path and os.path.exists(item.image_path): os.remove(item.image_path)
        return self.repo.delete(order)

    def _generate_number(self) -> str: return f"ORD-{self.repo.count() + 1:03d}"
    def _save_image(self, image) -> str:
        d = "static/uploads"; os.makedirs(d, exist_ok=True)
        p = f"{d}/{uuid.uuid4()}{os.path.splitext(image.filename)[1]}"
        with open(p, "wb") as f: shutil.copyfileobj(image.file, f)
        return p
