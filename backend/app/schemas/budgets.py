from pydantic import BaseModel
from decimal import Decimal

class BudgetCreate(BaseModel):
    category_id: int
    month: str  # YYYY-MM
    planned: Decimal

class BudgetOut(BudgetCreate):
    id: int
    class Config:
        from_attributes = True
