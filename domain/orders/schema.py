from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Optional, List

class OrderCreate(BaseModel):
    customer_name:  str   = Field(..., min_length=2, max_length=100)
    customer_phone: str   = Field("", max_length=20)
    customer_address: str = Field("", max_length=255) # عنوان العميل
    
    lengths:        List[float] = Field(...)
    widths:         List[float] = Field(...)
    prices_per_m2:  List[float] = Field(...)
    
    paid_amount:    float = Field(0, ge=0)
    payment_method: str   = Field("كاش")
    payment_ref:    str   = Field("")
    
    shipping_company: str = Field("", max_length=100) # شركة الشحن
    receipt_date:   Optional[date] = None # تاريخ الاستلام
    delivery_date:  Optional[date] = None # تاريخ التسليم
    notes:          str   = Field("", max_length=500)

    @field_validator("customer_name")
    def name_not_empty(cls, v):
        if not v.strip(): raise ValueError("اسم العميل مطلوب")
        return v.strip()

    @model_validator(mode='after')
    def validate_financials(self):
        if not (len(self.lengths) == len(self.widths) == len(self.prices_per_m2)):
            raise ValueError("يوجد خطأ في تطابق المقاسات مع الأسعار")
        total_price = round(sum((l * w) * p for l, w, p in zip(self.lengths, self.widths, self.prices_per_m2)), 2)
        if self.paid_amount > total_price and total_price > 0: raise ValueError("المدفوع يتجاوز الإجمالي")
        return self

class OrderUpdateStatus(BaseModel):
    new_status: str
