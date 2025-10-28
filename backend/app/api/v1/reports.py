from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...utils.deps import get_db, get_current_user
from ...db import models
from sqlalchemy import func
import csv, io
from fastapi.responses import StreamingResponse

router = APIRouter()

@router.get("/spend-by-category")
def spend_by_category(db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Sum negative amounts grouped by category via splits; fallback uncategorized
    # Simplified example: sum transaction amounts by sign
    income = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.user_id==user.id, models.Transaction.amount>0).scalar() or 0
    expense = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.user_id==user.id, models.Transaction.amount<0).scalar() or 0
    return {"income": float(income), "expense": float(expense)}

@router.get("/export.csv")
def export_csv(db: Session = Depends(get_db), user=Depends(get_current_user)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["date","account_id","payee","memo","amount","cleared"])
    for t in db.query(models.Transaction).filter(models.Transaction.user_id==user.id).all():
        writer.writerow([t.date, t.account_id, t.payee or "", t.memo or "", t.amount, t.cleared])
    output.seek(0)
    return StreamingResponse(iter([output.read()]), media_type="text/csv")
