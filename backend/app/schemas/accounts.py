from pydantic import BaseModel
from typing import Literal
from decimal import Decimal

class AccountCreate(BaseModel):
    name: str
    type: Literal["checking","savings","credit","cash"]
    currency: str = "USD"
    opening_balance: Decimal = Decimal("0.00")

class AccountOut(AccountCreate):
    id: int
    class Config:
        from_attributes = True
