from domain.orders.model import Order
from domain.orders.schema import OrderCreate, OrderUpdateStatus
from domain.orders.repository import OrderRepository
from config.constants import OrderStatus
import os
import shutil
import uuid


class OrderService:
    """
    مسؤوليته الوحيدة: Business Logic
    لا يعرف شيئاً عن HTTP أو قاعدة البيانات مباشرة
    """

    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def get_all(self, search: str = "", status: str = "") -> list[Order]:
        return self.repo.get_all(search=search, status=status)

    def get_stats(self) -> dict:
        return self.repo.get_stats()

    def create_order(self, data: OrderCreate, image=None) -> Order:
        # 1. حساب المساحة
        area = round(data.length * data.width, 2)

        # 2. توليد رقم الطلب
        number = self._generate_number()

        # 3. حفظ الصورة
        image_path = None
        if image and image.filename:
            image_path = self._save_image(image)

        # 4. إنشاء الطلب
        order = Order(
            number=number,
            customer_name=data.customer_name,
            customer_phone=data.customer_phone,
            length=data.length,
            width=data.width,
            area=area,
            notes=data.notes,
            delivery_date=data.delivery_date,
            image_path=image_path,
            status=OrderStatus.PENDING,
        )

        return self.repo.create(order)

    def update_status(self, order_id: int, data: OrderUpdateStatus) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"الطلب {order_id} مش موجود")
        order.status = data.new_status
        return self.repo.update(order)

    def delete_order(self, order_id: int) -> bool:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"الطلب {order_id} مش موجود")
        # احذف الصورة لو موجودة
        if order.image_path and os.path.exists(order.image_path):
            os.remove(order.image_path)
        return self.repo.delete(order)

    def _generate_number(self) -> str:
        count = self.repo.count() + 1
        return f"ORD-{count:03d}"

    def _save_image(self, image) -> str:
        upload_dir = "static/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        ext = os.path.splitext(image.filename)[1]
        filename = f"{uuid.uuid4()}{ext}"
        path = f"{upload_dir}/{filename}"
        with open(path, "wb") as f:
            shutil.copyfileobj(image.file, f)
        return path
