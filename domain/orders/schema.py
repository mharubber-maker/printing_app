from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Optional

class OrderCreate(BaseModel):
    customer_name:  str   = Field(..., min_length=2, max_length=100)
    customer_phone: str   = Field("", max_length=20)
    length:         float = Field(..., gt=0, le=100)
    width:          float = Field(..., gt=0, le=100)
    
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

    @field_validator("customer_phone")
    def phone_format(cls, v):
        if v and not v.replace(" ", "").isdigit(): raise ValueError("رقم التليفون غير صالح")
        return v.strip()

    @model_validator(mode='after')
    def validate_financials(self):
        # 1. منع الدفع الوهمي (المدفوع أكبر من الإجمالي)
        total = round((self.length * self.width) * self.price_per_m2, 2)
        if self.paid_amount > total and total > 0:
            raise ValueError(f"اختراق أمني: المبلغ المدفوع ({self.paid_amount}) يتجاوز الإجمالي ({total})")
            
        # 2. الإلزام المنطقي لبيانات التحويل
        electronic_methods = ["فودافون كاش", "انستا باي", "تحويل بنكي"]
        if self.payment_method in electronic_methods and not self.payment_ref.strip():
            raise ValueError(f"بيانات ناقصة: رقم العملية أو الموبايل مطلوب عند استخدام {self.payment_method}")
            
        return self

class OrderUpdateStatus(BaseModel):
    new_status: str
