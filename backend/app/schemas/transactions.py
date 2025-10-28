from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from decimal import Decimal

class SplitItem(BaseModel):
    category_id: int | None = None
    amount: Decimal

class TransactionCreate(BaseModel):
    account_id: int
    date: date
    payee: Optional[str] = None
    memo: Optional[str] = None
    amount: Decimal
    cleared: bool = False
    splits: List[SplitItem] = []

class TransactionOut(BaseModel):
    id: int
    account_id: int
    date: date
    payee: Optional[str]
    memo: Optional[str]
    amount: Decimal
    cleared: bool
    class Config:
        from_attributes = True
