from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import date
from typing import Optional, List

class OrderCreate(BaseModel):
    customer_name:  str   = Field(..., min_length=2, max_length=100)
    customer_phone: str   = Field("", max_length=20)
    
    lengths:        List[float] = Field(...)
    widths:         List[float] = Field(...)
    prices_per_m2:  List[float] = Field(...) # المصفوفة الجديدة للأسعار المتعددة
    
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
        if not (len(self.lengths) == len(self.widths) == len(self.prices_per_m2)):
            raise ValueError("يوجد خطأ في تطابق المقاسات مع الأسعار")
            
        # حساب ذكي: جمع (الطول × العرض × السعر) لكل سجادة
        total_price = round(sum((l * w) * p for l, w, p in zip(self.lengths, self.widths, self.prices_per_m2)), 2)
        
        if self.paid_amount > total_price and total_price > 0:
            raise ValueError(f"المبلغ المدفوع ({self.paid_amount}) يتجاوز الإجمالي ({total_price})")
            
        electronic_methods = ["فودافون كاش", "انستا باي", "تحويل بنكي"]
        if self.payment_method in electronic_methods and not self.payment_ref.strip():
            raise ValueError(f"رقم العملية مطلوب عند استخدام {self.payment_method}")
            
        return self

class OrderUpdateStatus(BaseModel):
    new_status: str
