from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...utils.deps import get_db, get_current_user
from ...db import models
from ...schemas.budgets import BudgetCreate, BudgetOut

router = APIRouter()

@router.post("", response_model=BudgetOut)
def create_budget(data: BudgetCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    b = models.Budget(user_id=user.id, **data.model_dump())
    db.add(b); db.commit(); db.refresh(b)
    return b

@router.get("", response_model=list[BudgetOut])
def list_budgets(month: str | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(models.Budget).filter(models.Budget.user_id == user.id)
    if month:
        q = q.filter(models.Budget.month == month)
    return q.all()
