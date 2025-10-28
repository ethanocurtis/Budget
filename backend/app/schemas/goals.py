from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class GoalCreate(BaseModel):
    category_id: int
    type: str
    target_amount: Decimal
    target_date: date | None = None

class GoalOut(GoalCreate):
    id: int
    class Config:
        from_attributes = True
