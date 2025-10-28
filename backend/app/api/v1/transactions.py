from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from ...utils.deps import get_db, get_current_user
from ...db import models
from ...schemas.transactions import TransactionCreate, TransactionOut, SplitItem
from decimal import Decimal
from typing import List
import os, csv, io
from ...core.config import settings

router = APIRouter()

@router.post("", response_model=TransactionOut)
def create_txn(data: TransactionCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Basic validation: ensure account belongs to user
    acct = db.query(models.Account).filter(models.Account.id==data.account_id, models.Account.user_id==user.id).first()
    if not acct:
        raise HTTPException(status_code=404, detail="Account not found")
    t = models.Transaction(user_id=user.id, account_id=data.account_id, date=data.date, payee=data.payee, memo=data.memo, amount=data.amount, cleared=data.cleared)
    db.add(t); db.commit(); db.refresh(t)
    # Splits
    for s in data.splits:
        db.add(models.Split(transaction_id=t.id, category_id=s.category_id, amount=s.amount))
    db.commit()
    return t

@router.get("", response_model=list[TransactionOut])
def list_txns(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Transaction).filter(models.Transaction.user_id==user.id).order_by(models.Transaction.date.desc()).all()

@router.post("/import-csv")
def import_csv(account_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    acct = db.query(models.Account).filter(models.Account.id==account_id, models.Account.user_id==user.id).first()
    if not acct:
        raise HTTPException(status_code=404, detail="Account not found")
    content = file.file.read().decode("utf-8")
    reader = csv.DictReader(io.StringIO(content))
    count = 0
    for row in reader:
        amount = Decimal(row.get("amount") or row.get("Amount") or "0")
        payee = row.get("payee") or row.get("Payee")
        memo = row.get("memo") or row.get("Memo")
        date = row.get("date") or row.get("Date")
        t = models.Transaction(user_id=user.id, account_id=acct.id, date=date, payee=payee, memo=memo, amount=amount, cleared=False)
        db.add(t); count += 1
    db.commit()
    return {"imported": count, "columns": reader.fieldnames}

@router.post("/{transaction_id}/attachments")
def upload_attachment(transaction_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    t = db.query(models.Transaction).filter(models.Transaction.id==transaction_id, models.Transaction.user_id==user.id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Transaction not found")
    os.makedirs(settings.media_root, exist_ok=True)
    dest = os.path.join(settings.media_root, file.filename)
    with open(dest, "wb") as f:
        f.write(file.file.read())
    a = models.Attachment(user_id=user.id, transaction_id=t.id, filename=file.filename, path=dest)
    db.add(a); db.commit()
    return {"msg": "uploaded", "id": a.id}
