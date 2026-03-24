from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Optional, List

class OrderCreate(BaseModel):
    customer_name:  str   = Field(..., min_length=2, max_length=100)
    customer_phone: str   = Field("", max_length=20)
    
    # تحويل الطول والعرض إلى قوائم (Arrays) لاستقبال أكثر من سجادة
    lengths:        List[float] = Field(...)
    widths:         List[float] = Field(...)
    
    price_per_m2:   float = Field(0, ge=0)
    paid_amount:    float = Field(0, ge=0)
    payment_method: str   = Field("كاش")
    payment_ref:    str   = Field("")
    
    notes:          str   = Field("", max_length=500)
    delivery_date:  Optional[date] = None

    @field_validator("customer_name")
    def name_not_empty(cls, v):
        if not v.strip(): raise ValueError("اسم العميل مطلوب")
        return v.strip()

    @model_validator(mode='after')
    def validate_financials(self):
        if len(self.lengths) != len(self.widths):
            raise ValueError("يوجد خطأ في تطابق الأطوال مع العروض")
            
        # حساب إجمالي المساحات لكل السجاد
        total_area = sum(l * w for l, w in zip(self.lengths, self.widths))
        total_price = round(total_area * self.price_per_m2, 2)
        
        if self.paid_amount > total_price and total_price > 0:
            raise ValueError(f"المبلغ المدفوع ({self.paid_amount}) يتجاوز الإجمالي ({total_price})")
            
        electronic_methods = ["فودافون كاش", "انستا باي", "تحويل بنكي"]
        if self.payment_method in electronic_methods and not self.payment_ref.strip():
            raise ValueError(f"رقم العملية مطلوب عند استخدام {self.payment_method}")
            
        return self

class OrderUpdateStatus(BaseModel):
    new_status: str
