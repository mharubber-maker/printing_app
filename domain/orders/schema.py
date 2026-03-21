from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional


class OrderCreate(BaseModel):
    customer_name:  str   = Field(..., min_length=2, max_length=100)
    customer_phone: str   = Field("", max_length=20)
    length:         float = Field(..., gt=0, le=100)
    width:          float = Field(..., gt=0, le=100)
    notes:          str   = Field("", max_length=500)
    delivery_date:  Optional[date] = None

    @validator("customer_name")
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("اسم العميل مطلوب")
        return v.strip()

    @validator("customer_phone")
    def phone_format(cls, v):
        if v and not v.replace(" ", "").isdigit():
            raise ValueError("رقم التليفون غلط")
        return v.strip()


class OrderUpdateStatus(BaseModel):
    new_status: str

    @validator("new_status")
    def valid_status(cls, v):
        from config.constants import OrderStatus
        if v not in OrderStatus.ALL:
            raise ValueError(f"الحالة غلط — المتاح: {OrderStatus.ALL}")
        return v


class OrderResponse(BaseModel):
    id:             int
    number:         str
    customer_name:  str
    customer_phone: Optional[str]
    length:         float
    width:          float
    area:           Optional[float]
    status:         str
    notes:          Optional[str]
    delivery_date:  Optional[date]
    image_path:     Optional[str]

    class Config:
        from_attributes = True
