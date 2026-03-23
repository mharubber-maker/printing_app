from sqlalchemy.orm import Session
from sqlalchemy import or_
from domain.orders.model import Order, Customer
from typing import Optional

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, search: str = "", status: str = "") -> list[Order]:
        query = self.db.query(Order).join(Order.customer, isouter=True)
        if search:
            query = query.filter(or_(Customer.name.ilike(f"%{search}%"), Order.number.ilike(f"%{search}%"), Customer.phone.ilike(f"%{search}%")))
        if status: query = query.filter(Order.status == status)
        return query.order_by(Order.created_at.desc()).all()

    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

    def count(self) -> int: return self.db.query(Order).count()

    def create(self, order: Order) -> Order:
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update(self, order: Order) -> Order:
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete(self, order: Order) -> bool:
        self.db.delete(order)
        self.db.commit()
        return True

    def get_stats(self) -> dict:
        all_orders = self.db.query(Order).all()
        return {
            "total": len(all_orders),
            "ongoing": sum(1 for o in all_orders if o.status == "جارى"),
            "ready": sum(1 for o in all_orders if o.status == "جاهز"),
            "delivered": sum(1 for o in all_orders if o.status == "تم التسليم"),
        }
