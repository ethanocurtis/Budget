from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...utils.deps import get_db, get_current_user
from ...db import models

router = APIRouter()

@router.get("/export")
def export_all(db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Simple JSON export of user-owned tables
    data = {
        "accounts": [a.__dict__ for a in db.query(models.Account).filter(models.Account.user_id==user.id).all()],
        "categories": [c.__dict__ for c in db.query(models.Category).filter(models.Category.user_id==user.id).all()],
        "category_groups": [g.__dict__ for g in db.query(models.CategoryGroup).filter(models.CategoryGroup.user_id==user.id).all()],
        "transactions": [t.__dict__ for t in db.query(models.Transaction).filter(models.Transaction.user_id==user.id).all()],
        "splits": [s.__dict__ for s in db.query(models.Split).join(models.Transaction, models.Split.transaction_id==models.Transaction.id).filter(models.Transaction.user_id==user.id).all()],
        "budgets": [b.__dict__ for b in db.query(models.Budget).filter(models.Budget.user_id==user.id).all()],
        "goals": [g.__dict__ for g in db.query(models.Goal).filter(models.Goal.user_id==user.id).all()],
        "attachments": [a.__dict__ for a in db.query(models.Attachment).filter(models.Attachment.user_id==user.id).all()],
        "audit_logs": [l.__dict__ for l in db.query(models.AuditLog).filter(models.AuditLog.user_id==user.id).all()],
    }
    # Remove SQLAlchemy internals
    for k, arr in data.items():
        for obj in arr:
            obj.pop("_sa_instance_state", None)
    return data
