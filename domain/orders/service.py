from domain.orders.model import Order, Customer, OrderItem, OrderImage
from domain.orders.schema import OrderCreate, OrderUpdateStatus
from domain.orders.repository import OrderRepository
from config.constants import OrderStatus
import os
import shutil
import uuid

class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def get_all(self, search: str = "", status: str = "") -> list[Order]:
        return self.repo.get_all(search=search, status=status)

    def get_stats(self) -> dict:
        return self.repo.get_stats()

    def create_order(self, data: OrderCreate, image=None) -> Order:
        number = self._generate_number()
        customer = Customer(name=data.customer_name, phone=data.customer_phone, notes=data.notes)
        order = Order(number=number, notes=data.notes, delivery_date=data.delivery_date, status=OrderStatus.PENDING, customer=customer)
        area = round(data.length * data.width, 2)
        item = OrderItem(length=data.length, width=data.width, area=area, description="طباعة")
        order.items.append(item)
        if image and image.filename:
            image_path = self._save_image(image)
            order.images.append(OrderImage(image_path=image_path))
        return self.repo.create(order)

    def update_status(self, order_id: str, data: OrderUpdateStatus) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order: raise ValueError(f"الطلب {order_id} مش موجود")
        order.status = data.new_status
        return self.repo.update(order)

    def delete_order(self, order_id: str) -> bool:
        order = self.repo.get_by_id(order_id)
        if not order: raise ValueError(f"الطلب {order_id} مش موجود")
        if order.images:
            for img in order.images:
                if os.path.exists(img.image_path): os.remove(img.image_path)
        return self.repo.delete(order)

    def _generate_number(self) -> str:
        count = self.repo.count() + 1
        return f"ORD-{count:03d}"

    def _save_image(self, image) -> str:
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        ext = os.path.splitext(image.filename)[1]
        path = f"{upload_dir}/{uuid.uuid4()}{ext}"
        with open(path, "wb") as f: shutil.copyfileobj(image.file, f)
        return path
