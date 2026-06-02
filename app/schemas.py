from pydantic import BaseModel

class PaymentCreate(BaseModel):
    amount: int
    merchant_order_id: str | None = None